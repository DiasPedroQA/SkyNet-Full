import React, { useEffect, useState, type JSX } from "react";

/**
 * Tipo que representa um item do sistema.
 * Pode ser um arquivo ou uma pasta.
 */
interface Item {
    id: string;
    name: string;
    type: "file" | "folder";
}

/**
 * URL base da API do backend (FastAPI)
 */
const API_URL: string = "http://localhost:8000/items";

/**
 * Componente principal da aplicação.
 */
function App(): JSX.Element {
    /**
     * Lista de itens retornados pela API.
     */
    const [items, setItems] = useState<Item[]>([]);

    /**
     * Estado controlado do campo nome.
     */
    const [name, setName] = useState<string>("");

    /**
     * Estado controlado do tipo (arquivo ou pasta).
     */
    const [type, setType] = useState<"file" | "folder">("file");

    /**
     * Armazena o ID do item em edição.
     * Se for null, significa que estamos criando.
     */
    const [editingId, setEditingId] = useState<string | null>(null);

    /**
     * Função responsável por buscar os itens da API.
     * Centralizamos aqui para poder reutilizar.
     */
    const fetchItems = async (): Promise<void> => {
        try {
            const response: Response = await fetch(API_URL);

            if (!response.ok) {
                throw new Error("Erro ao buscar itens");
            }

            const data: Item[] = await response.json();
            setItems(data);
        } catch (error) {
            console.error("Erro ao carregar itens:", error);
        }
    };

    /**
     * useEffect executado apenas na montagem do componente.
     * Serve para carregar os dados iniciais da API.
     */
    useEffect((): void => {
        fetchItems();
    }, []);

    /**
     * Manipulador de envio do formulário.
     * Usamos SubmitEvent (nativo do DOM) em vez de React.FormEvent,
     * pois React.FormEvent está marcado como deprecated nas novas definições.
     */
    const handleSubmit = async (e: React.SyntheticEvent): Promise<void> => {
        e.preventDefault();

        const itemData = {
            name,
            type,
        };

        try {
            if (editingId) {
                // Atualização (PUT)
                await fetch(`${API_URL}/${editingId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(itemData),
                });

                setEditingId(null);
            } else {
                // Criação (POST)
                await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(itemData),
                });
            }

            // Limpa formulário
            setName("");
            setType("file");

            // Recarrega lista após operação
            await fetchItems();
        } catch (error) {
            console.error("Erro ao salvar item:", error);
        }
    };

    /**
     * Coloca o item selecionado em modo de edição.
     */
    const handleEdit = (item: Item): void => {
        setName(item.name);
        setType(item.type);
        setEditingId(item.id);
    };

    /**
     * Remove item da API.
     */
    const handleDelete = async (id: string): Promise<void> => {
        try {
            await fetch(`${API_URL}/${id}`, {
                method: "DELETE",
            });

            await fetchItems();
        } catch (error) {
            console.error("Erro ao deletar item:", error);
        }
    };

    return (
        <div style={{ padding: "20px" }}>
            <h1>CRUD Arquivos e Pastas</h1>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nome"
                    value={name}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                        setName(e.target.value)
                    }
                    required
                />

                <select
                    value={type}
                    onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                        setType(e.target.value as "file" | "folder")
                    }
                >
                    <option value="file">Arquivo</option>
                    <option value="folder">Pasta</option>
                </select>

                <button type="submit">
                    {editingId ? "Atualizar" : "Criar"}
                </button>
            </form>

            <ul>
                {items.map((item: Item) => (
                    <li key={item.id}>
                        {item.type === "file" ? "📄" : "📁"} {item.name}
                        <button onClick={(): void => handleEdit(item)}>Editar</button>
                        <button onClick={() => { void handleDelete(item.id); }}>
                            Excluir
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
