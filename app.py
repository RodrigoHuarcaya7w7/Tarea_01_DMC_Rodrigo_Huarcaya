import streamlit as st
import numpy as np
import pandas as pd

from libreria_funciones_proyecto1 import calcular_wacc
from libreria_clases_proyecto1 import ProyectoInversion

# CONFIGURACIÓN GENERAL
st.set_page_config(page_title="Proyecto 1 - Python Fundamentals", page_icon="🐍", layout="centered")

# NAVEGACIÓN
st.sidebar.title(" Navegación")
seccion = st.sidebar.selectbox(
    "Selecciona una sección",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# HOME
if seccion == "Home":
    st.title("Proyecto Aplicado en Streamlit")
    st.subheader("Fundamentos de Programación - Módulo 1")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Nombre completo:** Rodrigo Huarcaya")
        st.markdown("**Módulo:** Python Fundamentals - Especialización en Python for Analytics")
    with col2:
        st.markdown("**Año:** 2026")
        st.markdown("**Institución:** DMC Institute")

    st.markdown("---")

    st.markdown("###  Descripción del proyecto")
    st.write(
        "Esta aplicación integra los conceptos fundamentales del Módulo 1: variables, "
        "estructuras de datos, control de flujo, funciones, programación funcional y "
        "programación orientada a objetos (POO). El enfoque temático de los ejercicios "
        "3 y 4 está orientado a **Ingeniería y Finanzas**, alineado con mi formación en "
        "Ingeniería de Sistemas de Información y mi experiencia en el área de Finanzas "
        "y Tesorería."
    )

    st.markdown("###  Tecnologías utilizadas")
    st.markdown(
        """
        - **Python 3**
        - **Streamlit** — interfaz interactiva
        - **NumPy** — manejo de arreglos
        - **Pandas** — estructuras de datos tipo DataFrame
        """
    )


# EJERCICIO 1 - FLUJO DE CAJA CON LISTAS

elif seccion == "Ejercicio 1":
    st.title("Ejercicio 1: Flujo de caja con listas")
    st.markdown(
        "Registra movimientos financieros (**ingresos** y **gastos**) en una lista. "
        "La aplicación calcula el total de ingresos, el total de gastos y el saldo final."
    )

    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []

    with st.form("form_movimiento", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            concepto = st.text_input("Concepto")
        with col2:
            tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        with col3:
            valor = st.number_input("Valor (S/)", min_value=0.0, step=10.0)

        agregar = st.form_submit_button("+ Agregar movimiento")

    if agregar:
        if concepto.strip() == "":
            st.error("El concepto no puede estar vacío.")
        elif valor <= 0:
            st.error("El valor debe ser mayor que cero.")
        else:
            st.session_state.movimientos.append(
                {"Concepto": concepto, "Tipo": tipo, "Valor (S/)": valor}
            )
            st.success(f"Movimiento '{concepto}' agregado correctamente.")

    st.markdown("---")
    st.markdown("###  Movimientos registrados")

    if len(st.session_state.movimientos) == 0:
        st.info("Aún no hay movimientos registrados.")
    else:
        df_mov = pd.DataFrame(st.session_state.movimientos)
        st.dataframe(df_mov, use_container_width=True)

        total_ingresos = df_mov.loc[df_mov["Tipo"] == "Ingreso", "Valor (S/)"].sum()
        total_gastos = df_mov.loc[df_mov["Tipo"] == "Gasto", "Valor (S/)"].sum()
        saldo_final = total_ingresos - total_gastos

        col1, col2, col3 = st.columns(3)
        col1.metric("Total ingresos", f"S/ {total_ingresos:,.2f}")
        col2.metric("Total gastos", f"S/ {total_gastos:,.2f}")
        col3.metric("Saldo final", f"S/ {saldo_final:,.2f}")

        if saldo_final >= 0:
            st.success(" El flujo de caja está A FAVOR.")
        else:
            st.error(" El flujo de caja está EN CONTRA.")

        if st.button(" Limpiar todos los movimientos"):
            st.session_state.movimientos = []
            st.rerun()


# EJERCICIO 2 - REGISTRO CON NUMPY, ARRAYS Y DATAFRAME

elif seccion == "Ejercicio 2":
    st.title("Ejercicio 2: Registro de productos con NumPy y DataFrame")
    st.markdown(
        "Registra productos o ventas. Cada registro se almacena primero como un "
        "**array de NumPy** y luego se convierte a un **DataFrame** actualizado en pantalla."
    )

    if "registros_np" not in st.session_state:

        st.session_state.registros_np = np.empty((0, 5), dtype=object)

    with st.form("form_producto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre_prod = st.text_input("Nombre del producto")
            categoria = st.selectbox("Categoría", ["Electrónica", "Alimentos", "Ropa", "Servicios", "Otro"])
        with col2:
            precio = st.number_input("Precio unitario (S/)", min_value=0.0, step=1.0)
            cantidad = st.number_input("Cantidad", min_value=0, step=1)

        agregar_prod = st.form_submit_button(" + Agregar registro") 

    if agregar_prod:
        if nombre_prod.strip() == "":
            st.error("El nombre del producto no puede estar vacío.")
        elif precio <= 0 or cantidad <= 0:
            st.error("El precio y la cantidad deben ser mayores que cero.")
        else:
            total = precio * cantidad
            nueva_fila = np.array([[nombre_prod, categoria, precio, cantidad, total]], dtype=object)
            st.session_state.registros_np = np.vstack([st.session_state.registros_np, nueva_fila])
            st.success(f"Registro '{nombre_prod}' agregado correctamente.")

    st.markdown("---")
    st.markdown("###  Registros (convertidos a DataFrame)")

    if st.session_state.registros_np.shape[0] == 0:
        st.info("Aún no hay registros.")
    else:
        df_prod = pd.DataFrame(
            st.session_state.registros_np,
            columns=["Producto", "Categoría", "Precio (S/)", "Cantidad", "Total (S/)"]
        )
        st.dataframe(df_prod, use_container_width=True)

        total_general = df_prod["Total (S/)"].astype(float).sum()
        st.metric("Total general", f"S/ {total_general:,.2f}")

        if st.button("🗑️ Limpiar todos los registros"):
            st.session_state.registros_np = np.empty((0, 5), dtype=object)
            st.rerun()


# EJERCICIO 3 - FUNCIÓN DESDE LIBRERÍA EXTERNA (FINANZAS: WACC)

elif seccion == "Ejercicio 3":
    st.title("Ejercicio 3: Cálculo del WACC")
    st.markdown(
        "Función seleccionada de `libreria_funciones_proyecto1.py`: **`calcular_wacc()`**, "
        "del área de **Finanzas**. Calcula el **Costo Promedio Ponderado de Capital (WACC)**, "
        "indicador clave para evaluar la rentabilidad mínima exigida de un proyecto de inversión."
    )

    st.markdown("###  Parámetros de entrada")
    col1, col2 = st.columns(2)
    with col1:
        deuda = st.number_input("Deuda (S/)", min_value=0.0, value=100000.0, step=1000.0)
        costo_deuda_pct = st.number_input("Costo de la deuda (%)", min_value=0.0, max_value=100.0, value=8.0)
        impuesto_pct = st.number_input("Tasa de impuesto (%)", min_value=0.0, max_value=100.0, value=29.5)
    with col2:
        patrimonio = st.number_input("Patrimonio (S/)", min_value=0.0, value=150000.0, step=1000.0)
        costo_patrimonio_pct = st.number_input("Costo del patrimonio (%)", min_value=0.0, max_value=100.0, value=15.0)

    if "historial_wacc" not in st.session_state:
        st.session_state.historial_wacc = []

    if st.button(" Ejecutar cálculo de WACC"):
        try:
            resultado = calcular_wacc(
                deuda=deuda,
                patrimonio=patrimonio,
                costo_deuda_pct=costo_deuda_pct,
                costo_patrimonio_pct=costo_patrimonio_pct,
                impuesto_pct=impuesto_pct
            )
            st.success(f"WACC calculado: **{resultado['wacc_pct']}%**")
            st.metric("WACC", f"{resultado['wacc_pct']} %")

            st.session_state.historial_wacc.append({
                "Deuda (S/)": deuda,
                "Patrimonio (S/)": patrimonio,
                "Costo Deuda (%)": costo_deuda_pct,
                "Costo Patrimonio (%)": costo_patrimonio_pct,
                "Impuesto (%)": impuesto_pct,
                "WACC (%)": resultado["wacc_pct"]
            })
        except ValueError as e:
            st.error(f"Error en los datos ingresados: {e}")

    st.markdown("---")
    st.markdown("###  Histórico de resultados")
    if len(st.session_state.historial_wacc) == 0:
        st.info("Aún no se han calculado resultados.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.historial_wacc), use_container_width=True)

        if st.button(" Limpiar histórico"):
            st.session_state.historial_wacc = []
            st.rerun()


# EJERCICIO 4 - CLASE DESDE LIBRERÍA EXTERNA CON CRUD (PROYECTO INVERSION)

elif seccion == "Ejercicio 4":
    st.title("Ejercicio 4: CRUD de Proyectos de Inversión")
    st.markdown(
        "Clase seleccionada de `libreria_clases_proyecto1.py`: **`ProyectoInversion`**, "
        "del área de **Finanzas**. Calcula **VPN**, **ROI** y **Payback simple**. "
        "A continuación se implementan las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)."
    )

    if "proyectos" not in st.session_state:
        st.session_state.proyectos = {}  

    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["➕ Crear", " Leer", " Actualizar", " Eliminar"]
    )


    with tab_crear:
        st.subheader("Crear nuevo proyecto")
        nombre_p = st.text_input("Nombre del proyecto", key="crear_nombre")
        inversion_p = st.number_input("Inversión inicial (S/)", min_value=0.0, value=10000.0, key="crear_inv")
        flujos_texto = st.text_input(
            "Flujos anuales (separados por coma)", value="4000, 4000, 4000", key="crear_flujos"
        )
        tasa_p = st.number_input(
            "Tasa de descuento (%)", min_value=0.0, max_value=100.0, value=10.0, key="crear_tasa"
        )

        if st.button("Crear proyecto"):
            try:
                flujos_lista = [float(x.strip()) for x in flujos_texto.split(",") if x.strip() != ""]
                proyecto = ProyectoInversion(nombre_p, inversion_p, flujos_lista, tasa_p)
                st.session_state.proyectos[nombre_p] = {
                    "inversion_inicial": inversion_p,
                    "flujos": flujos_lista,
                    "tasa_descuento_pct": tasa_p
                }
                st.success(f"Proyecto '{nombre_p}' creado correctamente.")
                st.json(proyecto.resumen())
            except ValueError as e:
                st.error(f"Error: {e}")

 
    with tab_leer:
        st.subheader("Proyectos registrados")
        if len(st.session_state.proyectos) == 0:
            st.info("Aún no hay proyectos registrados.")
        else:
            filas = []
            for nombre, datos in st.session_state.proyectos.items():
                p = ProyectoInversion(nombre, datos["inversion_inicial"], datos["flujos"], datos["tasa_descuento_pct"])
                filas.append(p.resumen())
            st.dataframe(pd.DataFrame(filas), use_container_width=True)

    with tab_actualizar:
        st.subheader("Actualizar un proyecto existente")
        if len(st.session_state.proyectos) == 0:
            st.info("No hay proyectos para actualizar.")
        else:
            nombre_sel = st.selectbox("Selecciona un proyecto", list(st.session_state.proyectos.keys()))
            datos_actuales = st.session_state.proyectos[nombre_sel]

            nueva_inversion = st.number_input(
                "Inversión inicial (S/)", min_value=0.0, value=float(datos_actuales["inversion_inicial"]), key="act_inv"
            )
            nuevos_flujos_texto = st.text_input(
                "Flujos anuales (separados por coma)",
                value=", ".join(str(f) for f in datos_actuales["flujos"]),
                key="act_flujos"
            )
            nueva_tasa = st.number_input(
                "Tasa de descuento (%)", min_value=0.0, max_value=100.0,
                value=float(datos_actuales["tasa_descuento_pct"]), key="act_tasa"
            )

            if st.button("Actualizar proyecto"):
                try:
                    nuevos_flujos = [float(x.strip()) for x in nuevos_flujos_texto.split(",") if x.strip() != ""]
                  
                    ProyectoInversion(nombre_sel, nueva_inversion, nuevos_flujos, nueva_tasa)
                    st.session_state.proyectos[nombre_sel] = {
                        "inversion_inicial": nueva_inversion,
                        "flujos": nuevos_flujos,
                        "tasa_descuento_pct": nueva_tasa
                    }
                    st.success(f"Proyecto '{nombre_sel}' actualizado correctamente.")
                except ValueError as e:
                    st.error(f"Error: {e}")

 
    with tab_eliminar:
        st.subheader("Eliminar un proyecto")
        if len(st.session_state.proyectos) == 0:
            st.info("No hay proyectos para eliminar.")
        else:
            nombre_del = st.selectbox("Selecciona un proyecto a eliminar", list(st.session_state.proyectos.keys()), key="del_sel")
            if st.button(" Eliminar proyecto", type="primary"):
                del st.session_state.proyectos[nombre_del]
                st.success(f"Proyecto '{nombre_del}' eliminado.")
                st.rerun()
