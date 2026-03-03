// frontend/components/FileCard.tsx
import React from 'react';
import { File } from '../types/file.types';
import Button from './Button';

interface FileCardProps {
  file: File;
  onDelete?: (id: number) => void;
  onDownload?: (id: number) => void;
}

const FileCard: React.FC<FileCardProps> = ({
  file,
  onDelete,
  onDownload,
}) => {
  const formatDate: (dateString: string) => string = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getFileIcon: (filename: string) => string = (filename: string) => {
    const ext: string | undefined = filename.split('.').pop()?.toLowerCase();
    const icons: Record<string, string> = {
      pdf: '📄',
      doc: '📝',
      docx: '📝',
      xls: '📊',
      xlsx: '📊',
      jpg: '🖼️',
      jpeg: '🖼️',
      png: '🖼️',
      gif: '🖼️',
      mp3: '🎵',
      mp4: '🎥',
      zip: '🗜️',
      rar: '🗜️',
    };
    return icons[ext || ''] || '📁';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      <div className="flex items-start space-x-4">
        <div className="text-4xl">{getFileIcon(file.name)}</div>

        <div className="flex-1">
          <h3 className="font-semibold text-lg truncate" title={file.name}>
            {file.name}
          </h3>

          <div className="text-sm text-gray-600 mt-1">
            <p>Tamanho: {file.size_formatted}</p>
            <p>Enviado: {formatDate(file.created_at)}</p>
          </div>

          <div className="flex space-x-2 mt-3">
            {onDownload && (
              <Button
                size="small"
                variant="secondary"
                onClick={() => onDownload(file.id)}
              >
                📥 Baixar
              </Button>
            )}

            {onDelete && (
              <Button
                size="small"
                variant="danger"
                onClick={() => onDelete(file.id)}
              >
                🗑️ Deletar
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileCard;
