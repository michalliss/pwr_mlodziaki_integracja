'use client'

import Image from "next/image";

import { Socket, io } from "socket.io-client"



export default function Home() {

  const socket = io('0.0.0.0:8000',  {
    path: '',
  });

  socket.on('connect', () => {
    console.log('Successfully connected!');
  });

  socket.connect();

  console.log("dupa")

  return (
    <div>
      {socket.connected ? <h1>Connected</h1> : <h1>Not connected</h1>}
      <h1>Next.js + TypeScript + Tailwind CSS</h1>
    </div>
  );
}
