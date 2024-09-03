import { Combobox, Autocomplete, useCombobox, TextInput, Stack, Text, Group } from "@mantine/core"
import React, { useEffect, useState } from "react"
const data = [
  'Dan', 'Mwangi', 'Stacy'
];

const InvoiceFooter: React.FC = () => {
  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });

  const [value, setValue] = useState('');
  const shouldFilterOptions = !data.some((item) => item === value);
  const filteredOptions = shouldFilterOptions
    ? data.filter((item) => item.toLowerCase().includes(value.toLowerCase().trim()))
    : data;

  const options = filteredOptions.map((item) => (
    <Combobox.Option value={item} key={item}>
      {item}
    </Combobox.Option>
  ));

  useEffect(() => {
    // we need to wait for options to render before we can select first one
    combobox.selectFirstOption();
  }, [value]);
  return (
    <div className="flex flex-wrap justify-between">
      <Combobox
        onOptionSubmit={(optionValue) => {
          setValue(optionValue);
          combobox.closeDropdown();
        }}
        store={combobox}
        withinPortal={false}
      >
        <Combobox.Target>
          <TextInput
            label="Billed by:"
            placeholder="Billed by"
            value={value}
            onChange={(event) => {
              setValue(event.currentTarget.value);
              combobox.openDropdown();
            }}
            onClick={() => combobox.openDropdown()}
            onFocus={() => combobox.openDropdown()}
            onBlur={() => combobox.closeDropdown()}
          />
        </Combobox.Target>

        <Combobox.Dropdown>
          <Combobox.Options>
            {options.length === 0 ? <Combobox.Empty>Nothing found</Combobox.Empty> : options}
          </Combobox.Options>
        </Combobox.Dropdown>
      </Combobox>
      <Stack>
        <Group>
          <Text>Total: </Text>
          <Text fw={500}> 500 Ksh </Text>
        </Group>

      </Stack>
    </div>
  )
}

export default InvoiceFooter
