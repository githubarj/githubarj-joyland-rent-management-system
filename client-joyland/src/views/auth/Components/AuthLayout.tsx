import { Container } from "@mantine/core"
import React from "react"
import { Outlet } from "react-router-dom"


const AuthLayout: React.FC = () => {
  return (
    <Container className="bg-slate-400">
      <Outlet />
    </Container >
  )
}


export default AuthLayout
