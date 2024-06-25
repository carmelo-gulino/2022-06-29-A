import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_album2 = None
        self.chosen_album1 = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_crea_grafo(self, e):
        try:
            n_canzoni = int(self.view.txt_n_canzoni.value)
        except ValueError:
            self.view.create_alert("Inserire un numero minimo di canzoni")
            return
        graph = self.model.build_graph(n_canzoni)
        self.fill_dds_album(graph)
        self.disable_elements()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Grafo con {len(graph.nodes)} nodi e {len(graph.edges)} archi"
                                                     f" creato"))
        self.view.update_page()

    def disable_elements(self):
        self.view.dd_album1.disabled = False
        self.view.dd_album2.disabled = False
        self.view.btn_adiacenze.disabled = False
        self.view.btn_percorso.disabled = False
        self.view.txt_soglia.disabled = False
        
    def fill_dds_album(self, graph):
        for album in graph.nodes:
            self.view.dd_album1.options.append(ft.dropdown.Option(data=album,
                                                                  text=album, 
                                                                  on_click=self.choose_album1))
            self.view.dd_album2.options.append(ft.dropdown.Option(data=album,
                                                                  text=album,
                                                                  on_click=self.choose_album2))
    
    def choose_album1(self, e):
        if e.control.data is None:
            self.chosen_album1 = None
        self.chosen_album1 = e.control.data
    
    def choose_album2(self, e):
        if e.control.data is None:
            self.chosen_album2 = None
        self.chosen_album2 = e.control.data

    def handle_adiacenze(self, e):
        if self.chosen_album1 is None:
            self.view.create_alert("Selezionare un album a1")
            return
        sorted_successors = self.model.get_sorted_successors(self.chosen_album1)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"I successori di {self.chosen_album1} "
                                                     f"in ordine di bilancio sono:"))
        for a in sorted_successors:
            self.view.txt_result.controls.append(ft.Text(f"{a[0]}, bilancio = {a[1]}"))
        self.view.update_page()

    def handle_percorso(self, e):
        if self.chosen_album1 is None or self.chosen_album2 is None:
            self.view.create_alert("Selezionare due album")
            return
        try:
            soglia = int(self.view.txt_soglia.value)
        except ValueError:
            self.view.create_alert("Inserire una soglia numerica")
            return
        path = self.model.get_percorso(self.chosen_album1, self.chosen_album2, soglia)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Percorso tra {self.chosen_album1} e {self.chosen_album2} "
                                                     f"di lunghezza {len(path)} trovato:"))
        for p in path:
            self.view.txt_result.controls.append(ft.Text(p))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
