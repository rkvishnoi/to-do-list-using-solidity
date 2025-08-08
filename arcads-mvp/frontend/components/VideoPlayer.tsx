"use client";
export default function VideoPlayer({ url }: { url: string }) {
  return (
    <video className="w-full rounded border" controls src={url} />
  );
}