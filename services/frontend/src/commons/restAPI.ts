import axios from 'axios';
import { API_BASE_URL, IS_PROD, VUE_APP_MOCK_SERVER_ENV } from "./constants";
import type { RestAPI } from "./interfaces";
import { mockAxios } from './axiosMock';

const IS_SERVER_RUNNING = IS_PROD || !VUE_APP_MOCK_SERVER_ENV;
const axiosInstance = axios.create({
    baseURL: IS_SERVER_RUNNING ? API_BASE_URL : '',
});

var restAPI: RestAPI = {
    writeErrorLogs: (log: any) => {
        console.error(log);
    },

    writeWarnLogs: (log: any) => {
        console.warn(log);
    },

    writeInfoLogs: (log: any) => {
        console.log(log);
    },

    getTauriAPI: async (request: string, context: string, base_url?: string) => {
        try {
            const axiosResult = await axiosInstance.get(request);
            return Promise.resolve(axiosResult);
        } catch (err) {
            return Promise.reject(err);
        }
    },

    postTauriAPI: async (request: string, context: string, playload?: any) => {
        try {
            const axiosResult = await axiosInstance.post(request, playload);
            return Promise.resolve(axiosResult);
        } catch (err) {
            return Promise.reject(err);
        }
    },

    putTauriAPI: async (request: string, context: string, playload: any) => {
        try {
            const axiosResult = await axiosInstance.put(request, playload);
            return Promise.resolve(axiosResult);
        } catch (err) {
            return Promise.reject(err);
        }
    }
};

//@ts-ignore
if (window.__TAURI__) {
    var invoke: any;
    var fetch: any;
    var ResponseType: any;
    var Body: any;
    // await is not available in the configured target env
    import('@tauri-apps/api').then((module) => invoke = module.invoke);
    import('@tauri-apps/api/http').then((module) => {
        fetch = module.fetch;
        ResponseType = module.ResponseType,
            Body = module.Body
    });

    restAPI.writeErrorLogs = function (log: any) {
        console.error(log);
        invoke('write_log', { log_message: `ERROR: ${log}` });
    }

    restAPI.writeWarnLogs = function (log: any) {
        console.warn(log);
        invoke('write_log', { log_message: `WARN: ${log}` });
    }

    restAPI.writeInfoLogs = function (log: any) {
        console.log(log);
        invoke('write_log', { log_message: `INFO: ${log}` });
    }

    restAPI.getTauriAPI = async function (request: string, context: string, base_url?: string): Promise<any> {
        const url = (base_url ?? API_BASE_URL) + request;
        this.writeInfoLogs(`get url : ${url}`);
        return await fetch(url, {
            method: "GET",
            //  responseType: ResponseType.JSON
        });
    }

    restAPI.postTauriAPI = async function (request: string, context: string, playload?: any): Promise<any> {
        const params: any = {
            method: "POST",
            responseType: ResponseType.JSON,
        }
        if (playload) {
            params.body = Body.json(playload);
        }
        const result = await fetch(API_BASE_URL + request, params);
        return result;
    }

    restAPI.putTauriAPI = async function (request: string, context: string, playload: any): Promise<any> {
        const params: any = {
            method: "PUT",
            body: Body.json(playload),
            responseType: ResponseType.JSON
        }
        return await fetch(API_BASE_URL + request, params);
    }
}
else if (!IS_SERVER_RUNNING) {
    restAPI.writeErrorLogs("Server is not connected, axios endpoints disabled, use this only for frontend development, and make sure to mock the API data you need");
    await mockAxios();
}

export { restAPI, axiosInstance };