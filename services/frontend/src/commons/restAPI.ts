import axios from 'axios';
import { API_BASE_URL, IS_PROD, SNACKBAR_TIMEOUT, VUE_APP_MOCK_SERVER_ENV } from "./constants";
import type { RestAPI } from "./interfaces";
import { mockAxios } from './axiosMock';
import { createPinia } from 'pinia';
const { vueApp } = useNuxtApp()

const pinia = createPinia();
vueApp.use(pinia);

const snackbarStore = useSnackbarStore();

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

    execGetAPI: async (request: string, context: string, base_url?: string) => {
        try {
            const axiosResult = await axiosInstance.get(request);
            return Promise.resolve(axiosResult);
        } catch (err) {
            return Promise.reject(err);
        }
    },

    execPostAPI: async (request: string, context: string, playload?: any) => {
        try {
            const axiosResult = await axiosInstance.post(request, playload);
            return Promise.resolve(axiosResult);
        } catch (err) {
            return Promise.reject(err);
        }
    },

    execPutAPI: async (request: string, context: string, playload: any) => {
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

    restAPI.execGetAPI = async function (request: string, context: string, base_url?: string): Promise<any> {
        const url = (base_url ?? API_BASE_URL) + request;
        this.writeInfoLogs(`get url : ${url}`);
        return await fetch(url, {
            method: "GET",
            //  responseType: ResponseType.JSON
        });
    }

    restAPI.execPostAPI = async function (request: string, context: string, playload?: any): Promise<any> {
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

    restAPI.execPutAPI = async function (request: string, context: string, playload: any): Promise<any> {
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

async function getAPI(request: string, context: string) {
    try {
        const getRes = await restAPI.execGetAPI(request, context);
        if (getRes.status !== 200) {
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        console.error(`error with the server, make sure it is started ${err}`);
        snackbarStore.setContent(`Error while ${context}, check the logs`, SNACKBAR_TIMEOUT, "error");
        restAPI.writeErrorLogs(`${request} : ${err}`);
    }
}

async function postAPI(request: string, context: string, playload?: any) {
    try {
        const getRes = await restAPI.execPostAPI(request, context, playload);
        if (getRes.status !== 200) {
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        snackbarStore.setContent(`Error while ${context}, check the logs`, SNACKBAR_TIMEOUT, "error");
        restAPI.writeErrorLogs(`${request} : ${err}`);
    }
}

async function putAPI(request: string, context: string, playload: any) {
    try {
        const getRes = await restAPI.execPutAPI(request, context, playload);
        if (getRes.status < 200 || getRes.status > 299) {
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        snackbarStore.setContent(`Error while ${context}, check the logs`, SNACKBAR_TIMEOUT, "error");
        restAPI.writeErrorLogs(`${request} : ${err}`);
    }
}

function writeErrorLogs(log: any) {
    restAPI.writeErrorLogs(log);
}

function writeWarnLogs(log: any) {
    restAPI.writeWarnLogs(log);
}

function writeInfoLogs(log: any) {
    restAPI.writeInfoLogs(log);
}

export { axiosInstance, getAPI, postAPI, putAPI, writeErrorLogs, writeWarnLogs, writeInfoLogs };