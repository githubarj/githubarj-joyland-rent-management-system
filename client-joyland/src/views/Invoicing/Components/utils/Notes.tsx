import { Textarea } from "@mantine/core";
import React from "react";

const Notes: React.FC = () => {
  return (
    <Textarea
      label="Notes"
      description="Additional comments"
      placeholder=""
    />
  )
}

export default Notes
