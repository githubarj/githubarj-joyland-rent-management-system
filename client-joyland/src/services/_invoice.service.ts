import { AxiosRequestConfig } from 'axios';
import { GET_INVOICES } from '../api/apis';
import request from '../api/request';

const getInvoices = (params?: AxiosRequestConfig<any>) => {
  return request.get(GET_INVOICES, params);
};

export const InvoiceService = { getInvoices };
