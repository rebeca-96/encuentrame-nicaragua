import os
import re
import hashlib
import uuid
from typing import Tuple
from io import BytesIO
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import HTTPException, status
from app.core.config import settings

# Ensure upload directory exists
os.makedirs(settings.STORAGE_DIR, exist_ok=True)

STORAGE_KEY_REGEX = re.compile(r"^(?:[a-f0-9]{32}|avatar_en-\d{4}-\d{4,5}|[a-zA-Z0-9_\-\.]{3,64})\.webp$")

VALID_IMAGE_SIGNATURES = [
    b"\xff\xd8\xff",       # JPEG
    b"\x89PNG\r\n\x1a\n",  # PNG
    b"RIFF",               # WebP (RIFF header)
    b"GIF87a", b"GIF89a"   # GIF
]

def sanitize_and_save_image(file_bytes: bytes, original_filename: str) -> Tuple[str, str]:
    """
    Sanitizes image by:
    1. Validating magic bytes / image signatures.
    2. Reading image bytes with Pillow in safe try-except.
    3. Completely stripping all EXIF metadata (GPS, device info, timestamps).
    4. Normalizing orientation if necessary.
    5. Resizing if dimensions exceed standard bounds (max 1280x1280).
    6. Saving as safe WebP image.
    7. Returning (storage_filename, sha256_hash).
    """
    if not file_bytes or len(file_bytes) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado está vacío o es demasiado pequeño."
        )

    # Validate header signature
    has_valid_signature = any(file_bytes.startswith(sig) for sig in VALID_IMAGE_SIGNATURES)
    if not has_valid_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no admitido. Debe ser una imagen válida (JPEG, PNG, WebP)."
        )

    # Calculate SHA256 of original file for audit verification
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    
    # Process image safely
    try:
        img = Image.open(BytesIO(file_bytes))
        img.verify() # Verify file integrity
        # Re-open after verify as verify closes/invalidates the image object
        img = Image.open(BytesIO(file_bytes))
    except (UnidentifiedImageError, Exception):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado no es una imagen válida o está dañado."
        )
    
    # Auto rotate if orientation tag exists, then discard all EXIF
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    
    # Discard EXIF by creating a clean RGB image
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    # Resize if too large
    max_dim = 1280
    if img.width > max_dim or img.height > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        
    # Generate unique storage filename
    unique_name = f"{uuid.uuid4().hex}.webp"
    save_path = os.path.join(settings.STORAGE_DIR, unique_name)
    
    # Save clean image without any EXIF tags
    img.save(save_path, format="WEBP", quality=85, optimize=True)
    
    return unique_name, sha256_hash

def get_file_path(storage_key: str) -> str:
    """
    Valida y resuelve la ruta segura de una fotografía almacenada.
    Previene de forma absoluta ataques de Path Traversal (CWE-22):
    1. Verifica que storage_key cumpla el formato hexadecimal estricto ^[a-f0-9]{32}\\.webp$
    2. Valida que la ruta canónica final resida estrictamente dentro de settings.STORAGE_DIR.
    """
    clean_key = storage_key.strip()
    if not clean_key or not STORAGE_KEY_REGEX.match(clean_key):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identificador de fotografía inválido. Formato no admitido."
        )

    base_dir = os.path.abspath(settings.STORAGE_DIR)
    full_path = os.path.abspath(os.path.join(base_dir, clean_key))

    if os.path.exists(full_path) and os.path.commonpath([base_dir, full_path]) == base_dir:
        return full_path

    # Buscar en directorios alternativos de avatares/imágenes si no está en uploads
    for alt in ["./frontend/public/images/avatars", "./frontend/out/images/avatars", "../frontend/public/images/avatars"]:
        alt_base = os.path.abspath(alt)
        alt_path = os.path.abspath(os.path.join(alt_base, clean_key))
        if os.path.exists(alt_path) and os.path.commonpath([alt_base, alt_path]) == alt_base:
            return alt_path

    return full_path
