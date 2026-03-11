interface invoiceData {
  id: number;
  houseNumber: string;
  tenant: string;
  total: number;
  issueDate: Date;
  balance: number;
  type: 'water' | 'rent' | 'repair' | 'expense';
}

export const invoicesData: invoiceData[] = [
  {
    id: 432,
    houseNumber: 'House 57',
    tenant: 'John Doe',
    total: 812,
    issueDate: new Date('2023-07-08'),
    balance: 309.1684169990121,
    type: 'rent',
  },
  {
    id: 748,
    houseNumber: 'House 43',
    tenant: 'Jane Smith',
    total: 571,
    issueDate: new Date('2022-07-08'),
    balance: 345.75159502007165,
    type: 'expense',
  },
  {
    id: 902,
    houseNumber: 'House 25',
    tenant: 'Michael Johnson',
    total: 319,
    issueDate: new Date('2024-04-08'),
    balance: 201.77700272946623,
    type: 'water',
  },
  {
    id: 512,
    houseNumber: 'House 70',
    tenant: 'Emily Brown',
    total: 269,
    issueDate: new Date('2024-07-08'),
    balance: 60.90507610370306,
    type: 'repair',
  },
  {
    id: 163,
    houseNumber: 'House 12',
    tenant: 'David Johnson',
    total: 450,
    issueDate: new Date('2024-01-08'),
    balance: 180.23896574054826,
    type: 'rent',
  },
  {
    id: 325,
    houseNumber: 'House 81',
    tenant: 'Sophia Wilson',
    total: 620,
    issueDate: new Date('2024-02-05'),
    balance: 425.6087400736936,
    type: 'expense',
  },
  {
    id: 897,
    houseNumber: 'House 36',
    tenant: 'James Brown',
    total: 380,
    issueDate: new Date('2023-08-08'),
    balance: 285.3376915305488,
    type: 'water',
  },
  {
    id: 742,
    houseNumber: 'House 63',
    tenant: 'Olivia Miller',
    total: 180,
    issueDate: new Date('2021-06-08'),
    balance: 110.65814062813184,
    type: 'repair',
  },
  {
    id: 578,
    houseNumber: 'House 48',
    tenant: 'Emma Martinez',
    total: 890,
    issueDate: new Date('2024-04-08'),
    balance: 600.2480487824552,
    type: 'rent',
  },
  {
    id: 49,
    houseNumber: 'House 4',
    tenant: 'Richard Githuba',
    total: 450,
    issueDate: new Date('2024-04-08'),
    balance: 0,
    type: 'rent',
  },
];
