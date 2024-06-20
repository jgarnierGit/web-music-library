import { defineEventHandler, defineLazyEventHandler } from 'h3'

export default defineLazyEventHandler(async () => {
    // @ts-expect-error TODO: https://github.com/nuxt/nuxt/issues/14131
    const { main } = await import('~/server/wasm/test.wasm')

    return defineEventHandler((event) => {
        getQuery(event);
        main();
    })
})
