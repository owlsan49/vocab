import service from "@/utils/request.js"

export function GetVocab(getParams){
    return service.request({
        method: "get",
        url: "/get_vocab",
        params: getParams
    })
}

export function GetInfoPost(url, postParams){
    return service.request({
        method: "post",
        url: url,
        data: postParams
    })
}