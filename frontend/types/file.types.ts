// frontend/types/file.types.ts
export interface File {
    id: number;
    name: string;
    path: string;
    size: number;
    size_formatted: string;
    user_id: number;
    created_at: string;
}

export interface FileUploadRequest {
    file: File;
    description?: string;
    is_public?: boolean;
}
