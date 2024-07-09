import { AxiosRequestConfig } from 'axios';
import { GET_INVOICES } from '../helpers/apis';
import request from '../helpers/request';

const getInvoices = (params?: AxiosRequestConfig<any>) => {
  return request.get(GET_INVOICES, params);
};

export const InvoiceService = { getInvoices };
