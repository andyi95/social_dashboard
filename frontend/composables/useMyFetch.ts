import useAuth from "~/store/useAuth";
import {UseFetchOptions} from "nuxt/app";
import {defu} from "defu";
import {useMessage} from "naive-ui";
import {FetchContext, FetchResponse} from "ofetch";
export function useMyFetch<T> (url: string,
                               options?: UseFetchOptions<T>) {
    const auth = useAuth();
    const config = useRuntimeConfig()
    const message = useMessage();

    const defaults: UseFetchOptions<T> = {
        baseURL: config.public.baseURL,
        headers: auth.$state.token? {Authorization: `Token ${auth.$state.token}`} : {},
        key: url,
        onResponseError(context: FetchContext & { response: FetchResponse<any> }): Promise<void> | void {
            if (context.response.status == 400){
                message.error(context.response.body? context.response.json() : 'Unknown Error')
            }
            console.log(error)
        },
        onRequestError(context: FetchContext & { error: Error }): Promise<void> | void {
            message.error(context.error.message, {closable: true})
            console.log(context)
            console.log(error)
        }
    }

    const params = defu(options, defaults)

    return useFetch(url, params)


                               }