'use client'

import Image from "next/image";
import { useEffect, useState } from "react";

import { Socket, io } from "socket.io-client"

const backend = "minikube.pl"

export default function Home() {

  const ws = new WebSocket('ws://' + backend + '/api/chat/ws');

  const [rooms, setRooms] = useState(null)
  const [newRoomName, setNewRoomName] = useState("")
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://' + backend + '/api/rooms/rooms')
      .then((res) => res.json())
      .then((data) => {
        setRooms(data.rooms)
        setLoading(false)
      })
  }, [])

  console.log("dupa")

  ws.addEventListener('open', (event) => {
    console.log(event)
  })

  ws.addEventListener('message', (event) => {
    console.log(event)
  })


  if (isLoading) return <p>Loading...</p>
  if (!rooms) return <p>No data</p>

  return (
    <div>
      <input onChange={(event) => setNewRoomName(event.target.value)}></input>
      <h1>{JSON.stringify(rooms)}</h1>
    </div>
  )
}
