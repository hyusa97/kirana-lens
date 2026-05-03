declare module 'humps' {
  export function camelizeKeys<T = any>(object: T): T;
  export function decamelizeKeys<T = any>(object: T): T;
}
