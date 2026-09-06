export interface UrlItem {
    id: number,
    short_code: string,
    original_url: string,
    created_at: string,
    short_url: string
}


export interface CreateUrlRequest {
    original_url: string
}