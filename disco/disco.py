class Sector:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.datos = ""
        self.ocupado = False

    def espacio_libre(self):
        return self.capacidad - len(self.datos.encode('utf-8'))


class DISCOLBA:
    def __init__(self, platos=2, pistas=10, sectores=100, tamano_sector=64):
        self.platos = platos
        self.superficies_por_plato = 2  # fijo a 2 superficies (superior e inferior)
        self.pistas = pistas
        self.sectores_por_pista = sectores
        self.tamano_sector = tamano_sector

        self.sectores_por_superficie = self.pistas * self.sectores_por_pista
        self.sectores_por_plato = self.superficies_por_plato * self.sectores_por_superficie
        self.total_sectores = self.platos * self.sectores_por_plato

        self.sectores = [Sector(tamano_sector) for _ in range(self.total_sectores)]
        self.mapa_ubicacion = {}  # {id_registro: [(lba_index, inicio_byte, fin_byte), ...]}

    def _lba_a_pps(self, lba_index):
        plato = lba_index // self.sectores_por_plato
        resto_plato = lba_index % self.sectores_por_plato

        superficie = resto_plato // self.sectores_por_superficie
        resto_superficie = resto_plato % self.sectores_por_superficie

        pista = resto_superficie // self.sectores_por_pista
        sector = resto_superficie % self.sectores_por_pista

        return plato, superficie, pista, sector

    def _pps_a_lba(self, plato, superficie, pista, sector):
        return (plato * self.sectores_por_plato
                + superficie * self.sectores_por_superficie
                + pista * self.sectores_por_pista
                + sector)

    def _buscar_primer_sector_libre(self):
        for i, sector in enumerate(self.sectores):
            if not sector.ocupado:
                return i
        return None

    def _buscar_siguiente_sector_contiguo(self, lba_actual):
        plato, superficie, pista, sector = self._lba_a_pps(lba_actual)

        sector += 1
        if sector >= self.sectores_por_pista:
            sector = 0
            pista += 1
            if pista >= self.pistas:
                pista = 0
                superficie += 1
                if superficie >= self.superficies_por_plato:
                    superficie = 0
                    plato += 1
                    if plato >= self.platos:
                        return None  # Se acabó espacio contiguo

        nuevo_lba = self._pps_a_lba(plato, superficie, pista, sector)

        if nuevo_lba >= self.total_sectores or self.sectores[nuevo_lba].ocupado:
            return None
        return nuevo_lba

    def guardar_dato(self, dato, id_registro):
        bytes_restantes = len(dato.encode('utf-8'))
        indice_dato = 0
        bloques_usados = []

        # Buscar primer sector libre para empezar contiguo
        lba_actual = self._buscar_primer_sector_libre()
        if lba_actual is None:
            raise MemoryError("Disco lleno, no hay espacio disponible.")

        while bytes_restantes > 0:
            sector = self.sectores[lba_actual]
            espacio_disponible = sector.espacio_libre()

            frag_bytes = dato.encode('utf-8')[indice_dato:indice_dato + espacio_disponible]
            frag_str = frag_bytes.decode('utf-8', errors='ignore')

            sector.datos += frag_str
            sector.ocupado = True

            inicio_byte = indice_dato
            fin_byte = indice_dato + len(frag_bytes) - 1

            bloques_usados.append((lba_actual, inicio_byte, fin_byte))

            bytes_restantes -= len(frag_bytes)
            indice_dato += len(frag_bytes)

            # Buscar siguiente sector contiguo libre
            if bytes_restantes > 0:
                lba_siguiente = self._buscar_siguiente_sector_contiguo(lba_actual)
                if lba_siguiente is None:
                    self._liberar_bloques(bloques_usados)
                    raise MemoryError("No hay suficiente espacio contiguo para guardar el dato completo.")
                lba_actual = lba_siguiente

        self.mapa_ubicacion[id_registro] = bloques_usados
        return True

    def _liberar_bloques(self, bloques):
        for (i, _, _) in bloques:
            sector = self.sectores[i]
            sector.datos = ""
            sector.ocupado = False

    def recuperar_dato(self, id_registro):
        if id_registro not in self.mapa_ubicacion:
            return None
        datos = []
        for (lba, ini, fin) in self.mapa_ubicacion[id_registro]:
            sector = self.sectores[lba]
            fragmento = sector.datos.encode('utf-8')[ini:fin + 1]
            datos.append(fragmento)
        return b"".join(datos).decode('utf-8', errors='ignore')

    def borrar_registro(self, id_registro):
        # No implementado porque dijiste que no hay borrado
        raise NotImplementedError("Borrado no está permitido en esta versión.")

    def mostrar_ubicacion_por_id(self):
        print("\n=== Ubicación de datos por ID ===")
        for id_registro, bloques in self.mapa_ubicacion.items():
            print(f"\nID: {id_registro}")
            for i, (lba, _, _) in enumerate(bloques, 1):
                plato, superficie, pista, sector = self._lba_a_pps(lba)
                fragmento = self.sectores[lba].datos
                print(f"  Bloque {i}: Plato {plato}, Superficie {superficie}, Pista {pista}, Sector {sector}")
                print(f"    Contenido: {fragmento[:20]}... ({len(fragmento.encode('utf-8'))} bytes)")

    def resumen_almacenamiento(self, id_registro):
        if id_registro not in self.mapa_ubicacion:
            return None
        bloques = self.mapa_ubicacion[id_registro]
        return f"Dato '{id_registro}' guardado en {len(bloques)} sectores."

    def detalle_almacenamiento(self, id_registro):
        if id_registro not in self.mapa_ubicacion:
            return None

        detalle = f"🔍 Detalles de almacenamiento - ID: {id_registro}\n\n"
        bloques = self.mapa_ubicacion[id_registro]
        dato_completo = self.recuperar_dato(id_registro)

        for i, (lba, ini, fin) in enumerate(bloques, 1):
            fragmento = self.sectores[lba].datos
            plato, superficie, pista, sector = self._lba_a_pps(lba)

            detalle += (
                f"🔹 Bloque {i}: LBA {lba} → Plato {plato}, Superficie {superficie}, Pista {pista}, Sector {sector}\n"
                f"   ▶ Bytes: {ini}-{fin}\n"
                f"   ▶ Fragmento: '{fragmento}'\n"
                f"   ▶ Tamaño: {len(fragmento.encode('utf-8'))} bytes\n"
                f"{'─'*40}\n"
            )

        detalle += f"\n📝 Dato completo reunido:\n{dato_completo}"
        return detalle
    
    def obtener_registro_formateado(self, id_registro):
        """
        Retorna la información del registro con ID `id_registro` en formato:
        {
            id_registro: {
                "contenido": dato completo,
                "ubicaciones": [(lba, inicio_byte, fin_byte), ...]
            }
        }
        """
        if id_registro not in self.mapa_ubicacion:
            return None

        bloques = self.mapa_ubicacion[id_registro]
        contenido_completo = self.recuperar_dato(id_registro)
        resultado = {
            id_registro: {
                "contenido": contenido_completo,
                "ubicaciones": []
            }
        }

        for (lba, ini, fin) in bloques:
            resultado[id_registro]["ubicaciones"].append(
                (lba, ini, fin)
            )

        return resultado
