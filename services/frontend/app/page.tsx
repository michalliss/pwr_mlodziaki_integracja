import Image from "next/image";

export default function Home() {
  return (
    <div>
      <h1>Next.js + TypeScript + Tailwind CSS</h1>
      <Image src="/nextjs.svg" alt="Next.js Logo" width={200} height={100} />
    </div>
  );
}
