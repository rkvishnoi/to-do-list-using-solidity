"use client";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

type Avatar = { id: string; name: string; thumbnail_url: string };

export default function AvatarPicker({ value, onChange }: { value?: string; onChange: (id: string) => void; }) {
  const [avatars, setAvatars] = useState<Avatar[]>([]);

  useEffect(() => { apiGet<Avatar[]>("/avatars").then(setAvatars).catch(console.error); }, []);

  return (
    <div className="grid grid-cols-2 gap-3">
      {avatars.map((a) => (
        <button key={a.id} onClick={() => onChange(a.id)} className={`border rounded p-2 flex items-center gap-3 hover:border-blue-500 ${value===a.id? 'border-blue-600' : ''}`}>
          <img src={a.thumbnail_url} alt={a.name} className="w-12 h-12 rounded object-cover" />
          <div className="text-left">
            <div className="font-medium">{a.name}</div>
            <div className="text-xs text-gray-500">{a.id}</div>
          </div>
        </button>
      ))}
    </div>
  );
}