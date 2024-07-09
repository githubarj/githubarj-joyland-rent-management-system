import { Tooltip, UnstyledButton } from '@mantine/core'
import React from 'react'
import { MdFullscreen, MdFullscreenExit } from 'react-icons/md';
import layout from '../../styles/layout.module.scss'
import { useFullscreen } from '@mantine/hooks';

const Fullscreen: React.FC = () => {
     const { toggle, fullscreen } = useFullscreen();
  return (
    <Tooltip
  label={!fullscreen ? 'Fullscreen' : 'Exit Fullscreen'}
      openDelay={500}
      transitionProps={{ transition: 'pop' }}
    >
      <UnstyledButton className={layout.centerIcons}>
        {fullscreen ? (
          <MdFullscreen size={24} onClick={toggle} />
        ) : (
          <MdFullscreenExit size={24} onClick={toggle} />
        )}
      </UnstyledButton>
    </Tooltip>
  );
}

export default Fullscreen
