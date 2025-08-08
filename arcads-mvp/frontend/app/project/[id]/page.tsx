export default function ProjectPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h1 className="text-xl font-semibold">Project {params.id}</h1>
      <p className="text-gray-600 mt-2">Detailed project view will go here.</p>
    </div>
  );
}