import create from "zustand";

interface AppState {
  serverUrl: string;
  setServerUrl: (url: string) => void;
}

export const useStore = create<AppState>((set) => ({
  serverUrl: "http://127.0.0.1:8080/api",
  setServerUrl: (url) => set((state) => ({ serverUrl: url })),
}));
