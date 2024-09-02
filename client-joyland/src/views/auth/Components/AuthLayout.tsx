import { Container } from "@mantine/core"
import React from "react"
import { Outlet } from "react-router-dom"


const AuthLayout: React.FC = () => {
  return (
    <Container fluid className=" h-screen bg-slate-200">
      <Outlet />
    </Container >
  )
}


export default AuthLayout
