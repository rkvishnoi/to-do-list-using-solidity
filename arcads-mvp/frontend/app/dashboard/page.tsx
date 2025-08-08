"use client";
import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
import AvatarPicker from "@/components/AvatarPicker";
import VideoPlayer from "@/components/VideoPlayer";

export default function DashboardPage() {
  const [projectId, setProjectId] = useState<number | null>(null);
  const [script, setScript] = useState<string>("Introducing our new product. It's fast, affordable, and effective!");
  const [language, setLanguage] = useState<string>("en");
  const [avatarId, setAvatarId] = useState<string>("");
  const [voicePreviewUrl, setVoicePreviewUrl] = useState<string>("");
  const [jobId, setJobId] = useState<number | null>(null);
  const [jobStatus, setJobStatus] = useState<string>("");
  const [videoUrl, setVideoUrl] = useState<string>("");

  async function previewVoice() {
    const res = await apiPost<{ url: string }>("/voices/preview", { text: script, language });
    setVoicePreviewUrl(res.url);
  }

  async function ensureProject() {
    if (projectId) return projectId;
    const created = await apiPost<{ id: number }>("/projects", { name: "My First Project" });
    setProjectId(created.id);
    return created.id;
  }

  async function generateVideo() {
    const pid = await ensureProject();
    // 1) Save script
    const created = await apiPost<{ id: number }>("/scripts", { project_id: pid, language, text: script });
    // 2) Create job
          const job = await apiPost<{ id: number; status: string }>("/jobs", { project_id: pid, script_id: created.id, avatar_id: avatarId });
setJobId(job.id);
    setJobStatus(job.status);
  }

  useEffect(() => {
    if (!jobId) return;
    const t = setInterval(async () => {
      const res = await apiGet<{ id: number; status: string; stage?: string; video_id?: number }>(`/jobs/${jobId}`);
      setJobStatus(`${res.status}${res.stage ? ` (${res.stage})` : ""}`);
      if (res.status === "completed" && res.video_id) {
        const signed = await apiGet<{ url: string }>(`/videos/${res.video_id}/signed-url`);
        setVideoUrl(signed.url);
        clearInterval(t);
      }
    }, 1500);
    return () => clearInterval(t);
  }, [jobId]);

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-3">
          <label className="block text-sm">Project ID</label>
          <input type="number" className="w-full border rounded p-2" value={projectId} onChange={(e)=>setProjectId(parseInt(e.target.value||"1"))} />
          <label className="block text-sm mt-4">Language</label>
          <input className="w-full border rounded p-2" value={language} onChange={(e)=>setLanguage(e.target.value)} />
          <label className="block text-sm mt-4">Script</label>
          <textarea className="w-full border rounded p-2 h-40" value={script} onChange={(e)=>setScript(e.target.value)} />
          <div className="flex gap-2">
            <button className="bg-gray-800 text-white px-3 py-2 rounded" onClick={previewVoice}>Preview Voice</button>
            <button className="bg-blue-600 text-white px-3 py-2 rounded" onClick={generateVideo}>Generate Video</button>
          </div>
          {voicePreviewUrl && (
            <audio src={voicePreviewUrl} controls className="w-full mt-3" />
          )}
          {jobId && (
            <div className="text-sm text-gray-600">Job {jobId}: {jobStatus}</div>
          )}
        </div>
        <div>
          <h2 className="font-semibold mb-2">Choose an Avatar</h2>
          <AvatarPicker value={avatarId} onChange={setAvatarId} />
        </div>
      </div>
      {videoUrl && (
        <div>
          <h2 className="font-semibold mb-2">Preview</h2>
          <VideoPlayer url={videoUrl} />
        </div>
      )}
    </div>
  );
}