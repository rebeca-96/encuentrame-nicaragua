"use client";

import { useEffect, useRef } from "react";
import { MapPoint } from "../../types";

interface MapProps {
  points: MapPoint[];
  center?: [number, number];
  zoom?: number;
}

export default function NicaraguaMap({
  points,
  center = [12.8654, -85.2072], // Centroid of Nicaragua
  zoom = 7,
}: MapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);

  useEffect(() => {
    // Dynamically import Leaflet in browser only
    if (typeof window === "undefined" || !mapContainerRef.current) return;

    let L: any;
    let map: any;

    import("leaflet").then((leafletModule) => {
      L = leafletModule.default || leafletModule;

      // Configurar iconos de Leaflet locales sin dependencias de CDN externos (unpkg/cdnjs)
      delete L.Icon.Default.prototype._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "/images/leaflet/marker-icon-2x.png",
        iconUrl: "/images/leaflet/marker-icon.png",
        shadowUrl: "/images/leaflet/marker-shadow.png",
      });

      // Avoid double initialization
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
      }

      map = L.map(mapContainerRef.current).setView(center, zoom);
      mapInstanceRef.current = map;

      // Clean CartoDB Positron or OpenStreetMap tiles for institutional appearance
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map);

      // Create Custom SVG Marker Icon
      const minorIcon = L.divIcon({
        className: "custom-div-icon",
        html: `<div style="background-color: #DC2626; width: 28px; height: 28px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 11px;">!</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      });

      const standardIcon = L.divIcon({
        className: "custom-div-icon",
        html: `<div style="background-color: #0F2A4A; width: 26px; height: 26px; border-radius: 50%; border: 3px solid #14B8A6; box-shadow: 0 2px 5px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; color: white; font-size: 10px;">•</div>`,
        iconSize: [26, 26],
        iconAnchor: [13, 13],
      });

      // Add markers for points
      points.forEach((pt) => {
        const marker = L.marker([pt.approximate_latitude, pt.approximate_longitude], {
          icon: pt.is_minor ? minorIcon : standardIcon,
        }).addTo(map);

        const dateStr = new Date(pt.disappearance_date).toLocaleDateString("es-NI");

        const popupContent = `
          <div style="font-family: Inter, sans-serif; padding: 4px; max-width: 240px;">
            <div style="font-size: 10px; font-weight: 700; color: ${pt.is_minor ? "#DC2626" : "#0F2A4A"}; text-transform: uppercase;">
              ${pt.is_minor ? "⚠️ ALERTA: MENOR DE EDAD" : "CASO ACTIVO"}
            </div>
            <div style="font-size: 13px; font-weight: 700; margin-top: 2px; color: #0F172A;">
              ${pt.full_name} (${pt.age_at_disappearance} años)
            </div>
            <div style="font-size: 11px; color: #475569; margin-top: 4px;">
              📍 <strong>${pt.municipality}, ${pt.department}</strong>
            </div>
            <div style="font-size: 11px; color: #64748B; margin-top: 2px;">
              🗓️ Última vez: ${dateStr}
            </div>
            <div style="font-size: 9px; color: #94A3B8; margin-top: 4px; font-style: italic;">
              * Ubicación geográfica agregada aproximada.
            </div>
            <div style="margin-top: 8px;">
              <a href="/casos/${pt.id}.html" style="display: inline-block; background-color: #0D9488; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; text-decoration: none; font-weight: 600;">
                Consultar ficha / Aportar pista
              </a>
            </div>
          </div>
        `;

        marker.bindPopup(popupContent);
      });
    });

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, [points, center, zoom]);

  return (
    <div className="relative w-full h-full min-h-[450px]">
      <div ref={mapContainerRef} className="w-full h-full min-h-[450px] shadow-inner" />
      
      {/* Map Legend Overlay */}
      <div className="absolute bottom-4 left-4 z-[400] bg-white/95 backdrop-blur-sm p-3 rounded-lg shadow-md border border-slate-200 text-xs">
        <div className="font-bold text-slate-800 mb-1.5">Leyenda del Mapa</div>
        <div className="flex items-center gap-2 mb-1">
          <span className="w-3.5 h-3.5 rounded-full bg-red-600 border border-white inline-block"></span>
          <span className="text-slate-700">Alerta Menor de Edad (NNA)</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3.5 h-3.5 rounded-full bg-[#0F2A4A] border-2 border-[#14B8A6] inline-block"></span>
          <span className="text-slate-700">Caso Activo Aprobado</span>
        </div>
        <div className="text-[10px] text-slate-600 mt-2 border-t pt-1 font-mono">
          Zonas representadas de forma aproximada.
        </div>
      </div>
    </div>
  );
}
