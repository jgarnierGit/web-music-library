import { API_BASE_URL } from './constants';

var writeErrorLogs = function (log: any) {
    console.error(`Tauri not launched, log is : ${log}`);
}

var writeWarnLogs = function (log: any) {
    console.warn(`Tauri not launched, log is : ${log}`);
}

var writeInfoLogs = function (log: any) {
    console.warn(`Tauri not launched, log is : ${log}`);
}

var getTauriAPI = async function (request: string, context: string): Promise<any> {
    console.warn("NOT IMPLEMENTED YET");
    return Promise.reject();
}

var postTauriAPI = async function (request: string, context: string, playload?: any): Promise<any> {
    console.warn("NOT IMPLEMENTED YET");
    return Promise.reject();
}

var putTauriAPI = async function (request: string, context: string, playload: any): Promise<any> {
    console.warn("NOT IMPLEMENTED YET");
    return Promise.reject();
}

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

    writeErrorLogs = function (log: any) {
        console.error(log);
        invoke('write_log', { log_message: `ERROR: ${log}` });
    }

    writeWarnLogs = function (log: any) {
        console.warn(log);
        invoke('write_log', { log_message: `WARN: ${log}` });
    }

    writeInfoLogs = function (log: any) {
        console.log(log);
        invoke('write_log', { log_message: `INFO: ${log}` });
    }

    getTauriAPI = async function (request: string, context: string): Promise<any> {
        return await fetch(API_BASE_URL + request, {
            method: "GET",
            responseType: ResponseType.JSON
        });
    }

    postTauriAPI = async function (request: string, context: string, playload?: any): Promise<any> {
        const params: any = {
            method: "POST",
            responseType: ResponseType.JSON
        }
        if (playload) {
            params.body = Body.json(playload);
        }
        return await fetch(API_BASE_URL + request, params);
    }

    putTauriAPI = async function (request: string, context: string, playload: any): Promise<any> {
        const params: any = {
            method: "PUT",
            body: Body.json(playload),
            responseType: ResponseType.JSON
        }
        return await fetch(API_BASE_URL + request, params);
    }
}
export { writeErrorLogs, writeWarnLogs, writeInfoLogs, getTauriAPI, postTauriAPI, putTauriAPI }