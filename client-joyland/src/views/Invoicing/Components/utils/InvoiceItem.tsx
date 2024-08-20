import { Button, CloseButton, Combobox, Input, InputBase, NumberInput, Tooltip, useCombobox } from '@mantine/core';
import React, { useState } from 'react'
import { IoAddSharp } from "react-icons/io5";

const groceries = ["Rent", "Water", "Repair"]

const InvoiceItem: React.FC = () => {
  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });

  const [value, setValue] = useState<string | null>(null);

  const options = groceries.map((item) => (
    <Combobox.Option value={item} key={item}>
      {item}
    </Combobox.Option>
  ));
  return (
    <>
      <div className='w-full flex justify-between p-4 rounded-md border'>
        <div className='flex flex-wrap gap-4 '>
          <Combobox
            store={combobox}
            onOptionSubmit={(val) => {
              setValue(val);
              combobox.closeDropdown();
            }}
          >
            <Combobox.Target>
              <InputBase
                label="Item"
                component="button"
                type="button"
                pointer
                rightSection={<Combobox.Chevron />}
                rightSectionPointerEvents="none"
                onClick={() => combobox.toggleDropdown()}
              >
                {value || <Input.Placeholder>Pick Item</Input.Placeholder>}
              </InputBase>
            </Combobox.Target>

            <Combobox.Dropdown>
              <Combobox.Options>{options}</Combobox.Options>
            </Combobox.Dropdown>
          </Combobox>
          <NumberInput
            label="Cost"
            placeholder="Cost (Ksh)"
          />
          <NumberInput
            label="Quantity"
            placeholder="Quantity"
          />
          <NumberInput disabled label="Total Cost" placeholder="Total Cost" />
        </div>
        <div className=''>
          <Tooltip label="Remove item">
            <CloseButton size={"sm"} />
          </Tooltip>
        </div>
      </div>
      <Button variant="filled" className='mt-2.5' rightSection={<IoAddSharp size={18} />}>Add an item</Button>
    </>
  )
}

export default InvoiceItem 
