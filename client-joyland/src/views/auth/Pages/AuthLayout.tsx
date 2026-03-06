import { Container } from "@mantine/core"
import React from "react"
import { Outlet } from "react-router-dom"
import authLayout from "../styles/authLayout.module.scss"

const AuthLayout: React.FC = () => {
  return (
    <Container fluid className={`${authLayout.background} flex items-center  h-screen`}>
      <Outlet />
    </Container >
  )
}


export default AuthLayout
