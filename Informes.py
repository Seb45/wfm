import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import time
import sqlite3
import datetime as dt
import subprocess
import numpy as np
from getpass import getuser
import plotly.graph_objects as go

colores=['black', 'red', 'olive','gray', 'blue', 'orange', 'green', 'purple', 'brown',  'cyan', 'green', 'blue', 'violet']


def grafico_individual(data_uno):

  		# data_uno=pd.read_sql('SELECT datetime(fechahora/1000, "unixepoch", "localtime") as fechahora, close, q_inf, q_sup, q_mediana, rsi from coin_15minute where coin ="'+coin_select+'"order by fechahora', con)
        data_uno=data_uno.reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_uno['intervalo'], y=data_uno['Atencion'],line=dict(color='green', width=4), name='Atencion'))
          
          
  		# fig.add_trace(go.Scatter(x=data_uno['fechahora'], y=data_uno['q_inf'],
  		# 		    line=dict(color='red', width=2, dash='dash'),
  		# 		    name='q_inf'))
  		# fig.add_trace(go.Scatter(x=data_uno['fechahora'], y=data_uno['q_mediana'],
  		# 		    line=dict(color='orange', width=2, dash='dash'),
  		# 		    name='q_mediana'))     
  		# fig.add_trace(go.Scatter(x=data_uno['fechahora'], y=data_uno['q_sup'],
  		# 		    line=dict(color='blue', width=2, dash='dash'),
  		# 		    name='q_sup'))   
  		# fig.add_trace(go.Scatter(x=data_uno['fechahora'], y=data_uno['ta_os_BB_upperband'],
  		# 		    line=dict(color='green', width=2, dash='dash'),
  		# 		    name='ta_os_BB_upperband'))    
  		# fig.add_trace(go.Scatter(x=data_uno['fechahora'], y=data_uno['ta_os_BB_lowerband'],
  		# 		    line=dict(color='black', width=1, dash='dot'),
  		# 		    name='ta_os_BB_lowerband'))  


        fig.update_xaxes(type='category')
        fig.update_layout(height=650, width=1200)
        st.plotly_chart(fig, use_container_width=True)

def cmd(comando, ip):
    subprocess.run(comando+ip, shell=True)
   
con = sqlite3.connect("wfm_nice.db")
cursorobj=con.cursor()


    
informe = st.sidebar.selectbox(
    'Elegí uno de los informes disponibles',
    ('Cantidad por intervalo', 'otro')
)

if informe=="Utilizacion":
    data_plataformas=pd.read_sql('SELECT * from s_q_plataforma_tipo', con)
    data_plataformas_presencial=pd.read_sql('SELECT * from s_q_plataforma_tipo_presencial', con)
    data_plataformas_remoto=pd.read_sql('SELECT * from s_q_plataforma_tipo_remoto', con)

    data_servicio=pd.read_sql('SELECT * from s_q_servicio_tipo', con)
    data_pivot=data_plataformas.pivot(index='Plataforma', columns='tipo_conexion_xml', values='ip')
    data_pivot=data_pivot.fillna(0)
    data_total=data_pivot.sum()
    data_pivot["Total"]=data_pivot["Red_Externa"]+data_pivot["Apagadas"]+data_pivot["Libres"]+data_pivot["Remoto"]+data_pivot["Presencial"]
    
    data_pivot_servicio=data_servicio.pivot(index='grupo', columns='tipo_conexion_xml', values='ip')
    data_pivot_servicio=data_pivot_servicio.fillna(0)
    data_pivot_servicio_sum=data_pivot_servicio.sum()
    data_pivot_servicio["Total"]=data_pivot_servicio["Red_Externa"]+data_pivot_servicio["Apagadas"]+data_pivot_servicio["Libres"]+data_pivot_servicio["Remoto"]+data_pivot_servicio["Presencial"]
 

    data_plataformas_presencial_pivot=data_plataformas_presencial.pivot(index='Plataforma', columns='tipo_conexion_xml', values='ip')
    data_plataformas_presencial_pivot=data_plataformas_presencial_pivot.fillna(0)
    data_plataformas_presencial_pivot_sum=data_plataformas_presencial_pivot.sum()

    data_plataformas_remoto_pivot=data_plataformas_remoto.pivot(index='Plataforma', columns='tipo_conexion_xml', values='ip')
    data_plataformas_remoto_pivot=data_plataformas_remoto_pivot.fillna(0)
    data_plataformas_remoto_pivot_sum=data_plataformas_remoto_pivot.sum()

    data_detalle_ip=pd.read_sql('SELECT * from s_plat_tipo_grupo_modo_detalle where grupo in ("COVID", "METLIFE") order by 4, 2,1', con)

    st.text(f"Informacion actualizada a: {fecha_act.iloc[0,0]} ({fecha_act.iloc[0,1]} minutos)")
      
    #data_total.rename(columns={'0':'PCs'})
  
    col1, col2 = st.beta_columns([3,6])
    with col1:
        st.dataframe(data=data_total)
    with col2:
        st.bar_chart(data_total)
    
    with st.beta_expander("Ver detalle por plataforma"):
    
        st.dataframe(data=data_pivot, width=900, height=500)
    
    with st.beta_expander("Ver detalle por servicios"):
    
        st.dataframe(data=data_pivot_servicio, width=900, height=900)

    with st.beta_expander("Ver detalle Presencial"):
    
        st.dataframe(data=data_plataformas_presencial_pivot, width=900, height=900)
        tupla_plataformas=tuple(data_plataformas_presencial_pivot.index)
        plat_presencial=st.selectbox("Plataforma", tupla_plataformas)
        data_plataformas_presencial_grupo_modo=pd.read_sql('SELECT grupo, tipo_conexion_xml, ip from s_q_plataforma_tipo_presencial_grupo_modo where Plataforma="'+plat_presencial+'"', con)
        data_plat_pres_grupo_modo_pivot=data_plataformas_presencial_grupo_modo.pivot(index='grupo', columns='tipo_conexion_xml', values='ip')
        data_plat_pres_grupo_modo_pivot=data_plat_pres_grupo_modo_pivot.fillna(0)
        
        st.dataframe(data=data_plat_pres_grupo_modo_pivot, width=900, height=900)
        
    with st.beta_expander("Ver detalle Remoto"):
    
        st.dataframe(data=data_plataformas_remoto_pivot, width=900, height=900)
        
    
    data_vdi_remoto_presencial=pd.read_sql('SELECT * from s_vdi_remoto_presencial', con)
    data_vdi_remoto_presencial_pivot=data_vdi_remoto_presencial.pivot(index='plataforma', columns='modo', values='cantidad')
    data_vdi_remoto_presencial_pivot=data_vdi_remoto_presencial_pivot.fillna(0)
    with st.beta_expander("Ver detalle VDI habilitado"):
    
        st.dataframe(data=data_vdi_remoto_presencial_pivot, width=900, height=900)
        
    with st.beta_expander("Ver detalle IP Covid/Metlife"):
    
        st.dataframe(data=data_detalle_ip, width=900, height=900)  
    #st.bar_chart(data=data_pivot)
    
    #chart_data = pd.DataFrame(np.random.randn(10, 3),columns=["a", "b", "c"])
    #st.bar_chart(chart_data)
    #st.dataframe(data=chart_data, width=900, height=500)



if informe=="Ultimo Estado":
    data_ultimo_estado=pd.read_sql('SELECT * from s_ultimoestado_pc', con)
  
    st.text(f"Ultima actualizacion proceso PC: {fecha_proceso.iloc[0,0]} ({fecha_proceso.iloc[0,1]} minutos)")    
    st.text(f"Ultimo estado PCs              : {fecha_act.iloc[0,0]} ({fecha_act.iloc[0,1]} minutos)")
      
    data_ultimo_estado=data_ultimo_estado.set_index("Plataforma")
    
    st.dataframe(data=data_ultimo_estado)
    data_ultimo_estado=data_ultimo_estado.drop(columns=["cantidad"])
    data_ultimo_estado["objetivo"]=10
    st.line_chart(data_ultimo_estado)
    

    #st.bar_chart(data=data_pivot)
    
    #chart_data = pd.DataFrame(np.random.randn(10, 3),columns=["a", "b", "c"])
    #st.bar_chart(chart_data)
    #st.dataframe(data=chart_data, width=900, height=500)
if informe=="Lista Negra":
    
    
    radio_listanegra = st.sidebar.radio(
        "",
        ('Lista Negra actual', 'Lista Negra historica liberada', 'registro IP ocupada', 'Lista Negra Reiterada'))
    

        
    if radio_listanegra == 'Lista Negra actual':
       
        
        fecha_act=pd.read_sql('select max(UltimoEstado) as fecha from base_pcs', con)
     
        data_lista_negra=pd.read_sql('SELECT distinct ip, fecha, ticket, comentarios, usuario from listanegra_Pc where usuario<>"scedermas" order by fecha desc', con)
      
        
        st.text(fecha_act.iloc[0,0])

        data_lista_negra.reset_index(drop=True, inplace=True)        
        st.dataframe(data=data_lista_negra, width=1450)
        
        ip_lista_negra_eliminar=st.text_input('Liberar IP de lista negra: ', value="")
        
        liberar_ip=st.button('Liberar')
        
        if liberar_ip:
            cursorobj.execute('insert into listanegra_Pc_log select * from listanegra_Pc where ip="'+str(ip_lista_negra_eliminar)+'";')
            con.commit() 
            cursorobj.execute('delete from listanegra_Pc where ip="'+str(ip_lista_negra_eliminar)+'";')
            con.commit() 
        
    elif radio_listanegra == 'Lista Negra historica liberada':  
        data_lista_negra_log=pd.read_sql('SELECT * from listanegra_Pc_Log order by fecha desc', con)
        data_lista_negra_log.reset_index(drop=True, inplace=True)
        
        st.text(data_lista_negra_log)         
    elif radio_listanegra == 'registro IP ocupada':  
        data_lista_ocup=pd.read_sql('SELECT * from listaocupada_Pc order by fecha desc', con)
        data_lista_ocup_resumen=pd.read_sql('SELECT substr(fecha,1,10) as fecha, count(distinct usuario) as usuarios from listaocupada_Pc group by substr(fecha,1,10) order by 1 desc', con)
        data_lista_ocup_resumen.reset_index(drop=True, inplace=True)        
        st.text(data_lista_ocup_resumen)              
        st.dataframe(data_lista_ocup)             
    elif radio_listanegra == 'Lista Negra Reiterada':  
        data_lista_reit=pd.read_sql('SELECT * from s_lista_negra_reit', con)
        st.header('IPs con mas cantidad de ingresos en lista negra en los ultimos 10 dias')
        st.table(data_lista_reit)              

if informe=="Asignaciones":
    
    ip_buscar = st.text_input("ingresá la IP", value="", max_chars=15)
    if len(ip_buscar)>0:
        data_log_solicitud=pd.read_sql('SELECT substr(fechaHora, 1, 19) as fechahora, dni_usuario, tipo_imagen, sist_operativo, usuario from log_solicitudes where ip_asignada="'+ip_buscar+'" order by FechaHora desc', con)
        if len(data_log_solicitud)>0:
            data_log_solicitud=data_log_solicitud.set_index('fechahora')
            st.table(data=data_log_solicitud)
        else:
            st.text("no se encontraron asignaciones para esta IP")
    else:
        st.text("Últimas 25 asignaciones:")
        data_log_solicitud_t=pd.read_sql('SELECT substr(fechaHora, 1, 19) as fechahora, dni_usuario, tipo_imagen, sist_operativo, ip_asignada, usuario from log_solicitudes order by FechaHora desc limit 25', con)
        data_log_solicitud_t=data_log_solicitud_t.set_index('fechahora')
        st.dataframe(data=data_log_solicitud_t)

    st.subheader("Utilización diaria (cantidad de asignaciones)")        
    data_uso_web=pd.read_sql('SELECT * from s_uso_web', con)
    data_uso_web=data_uso_web.set_index('fecha')
    st.line_chart(data_uso_web)

    
    data_asignaciones=pd.read_sql('SELECT fecha, tipo, cant from s_resumen_logica_asignacion', con)
    data_asignaciones_pivot=data_asignaciones.pivot(index='fecha', columns='tipo', values='cant')
    data_asignaciones_pivot=data_asignaciones_pivot.fillna(0)
    st.subheader("Funcionamiento logica asignacion web")
    st.table(data_asignaciones_pivot.sort_index(ascending=False))  

    data_uso_ip=pd.read_sql('SELECT * from s_histograma_uso_Ips', con)
    data_uso_ip=data_uso_ip.set_index('cant_usuarios')
    st.line_chart(data_uso_ip)
    
    data_uso_usuarios=pd.read_sql('SELECT * from s_histograma_uso_usuarios', con)
    data_uso_usuarios=data_uso_usuarios.set_index('cant_ip')
    st.line_chart(data_uso_usuarios)

if informe=="Utilizacion historica":
    radio_plataf = st.sidebar.radio(
        "",
        ('Total (sin VDI)', 'por Plataforma', 'por IP', 'por Usuario', 'Detalle'))
    

        
    if radio_plataf == 'Total (sin VDI)':
       
        data_plat_histo=pd.read_sql('select fecha_hora, tipo, sum(cantidad) as cantidad from q_plataforma_tipo where plataforma<>"VDI" and julianday(fecha_hora)>julianday(datetime("now","localtime"))-4 group by fecha_hora, tipo', con)
    
        data_pivot_histo=data_plat_histo.pivot(index='fecha_hora', columns='tipo', values='cantidad')
        data_pivot_histo=data_pivot_histo.fillna(0)
        data_pivot_histo_sum=data_pivot_histo.sum()
        #st.line_chart(data=data_pivot_histo)
        data_pivot_histo=data_pivot_histo.sort_index(ascending=False)
        data_pivot_histo["Total"]=0
        for fila in range(data_pivot_histo.shape[0]):
            for columna in range(data_pivot_histo.shape[1]-1):
                data_pivot_histo.iloc[fila,data_pivot_histo.shape[1]-1]+=data_pivot_histo.iloc[fila,columna]
        #st.line_chart(data=data_pivot_histo)
        st.dataframe(data_pivot_histo.head(200))
        datos_graficos=pd.DataFrame()
        datos_graficos["Ocupados"]=data_pivot_histo["Remoto"]+data_pivot_histo["Presencial"]
        datos_graficos["Libres"]=data_pivot_histo["Libres"]
        #st.dataframe(datos_graficos)
        st.line_chart(datos_graficos)
        
    elif radio_plataf == 'Detalle':
       
        # data_detalle_histo=pd.read_sql('select * from q_plat_tipo_grupo_modo_so_histo order by 1 desc ,2,3,4,5 desc limit 1000 ', con)
    
        # st.dataframe(data_detalle_histo)
        
        
        
        
        data_plataformas2=pd.read_sql('select distinct upper(plataforma) as plataforma from q_plat_tipo_grupo_modo_so_histo order by 1', con)
        tupla_plataformas2=tuple(data_plataformas2['plataforma'])
        #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
        data_grupo=pd.read_sql('select distinct upper(grupo) as grupo from s_grupos', con)
        tupla_grupo=tuple(data_grupo['grupo'])   
           
        col1, col2 = st.beta_columns([3,3])
        with col1:
            plataforma_select_dispo2=st.multiselect("Plataforma", tupla_plataformas2)
            modo_select_dispo2=st.radio("Modo", ['Remoto', 'Presencial'])       

        with col2:
            grupo_select=st.multiselect("Imagen", tupla_grupo)
            estado_select_dispo2=st.multiselect("Estado Uso", ['Apagadas', 'Libres', 'Presencial', 'Remoto'])
          
        texto2=""
        texto3=""
        texto4=""
        for i in range(len(plataforma_select_dispo2)):
            texto2+='"'
            texto2+=plataforma_select_dispo2[i]
            texto2+='",'
        texto2+='""'
        for i in range(len(estado_select_dispo2)):
            texto3+='"'
            texto3+=estado_select_dispo2[i]
            texto3+='",'
        texto3+='""'
        for i in range(len(grupo_select)):
            texto4+='"'
            texto4+=grupo_select[i]
            texto4+='",'
        texto4+='""'
        # st.text(texto2)     
        
        if texto2=="":
            st.subheader("Elegi al menos una plataforma")
        else:
            data_dispo2=pd.read_sql('SELECT * from s_q_uso_histo where upper(plataforma) in( '+texto2+') and  Modo="'+modo_select_dispo2+'" and tipo in( '+texto3+') and grupo in( '+texto4+') order by 1 desc, 2,3,4,5 limit 300', con)
            st.table(data=data_dispo2)
            







            
        
    elif radio_plataf == 'por IP':
        ip_buscar_histo=st.text_input('Ingresa IP a buscar su historico de uso:')
        if len(ip_buscar_histo)>0:

            
            data_ip_histo=pd.read_sql('select fechahoradesde, fechahorahasta, username from s_log_ip_usuario where ip="'+ip_buscar_histo+'"', con)
            st.table(data=data_ip_histo)
            
    elif radio_plataf == 'por Usuario':
        usuario_buscar_histo=st.text_input('Ingresa Usuario a buscar su historico de uso:')
        if len(usuario_buscar_histo)>0:

            
            data_usuario_histo=pd.read_sql('select fechahoradesde, fechahorahasta, IP from s_log_ip_usuario where username="'+usuario_buscar_histo.upper()+'"', con)
            st.text(data_usuario_histo)

    else:   
        data_plataformas=pd.read_sql('select distinct plataforma from q_plataforma_tipo order by 1', con)
        tupla_plataformas=tuple(data_plataformas['plataforma'])
        #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
        plataforma_select=st.sidebar.radio("Plataforma", tupla_plataformas)
        
        data_plat_histo=pd.read_sql('select fecha_hora, tipo, cantidad  from q_plataforma_tipo where plataforma in ("'+plataforma_select+'")  and julianday(fecha_hora)>julianday(datetime("now","localtime"))-4 ', con)
    
        data_pivot_histo=data_plat_histo.pivot(index='fecha_hora', columns='tipo', values='cantidad')
        data_pivot_histo=data_pivot_histo.fillna(0)
        data_pivot_histo_sum=data_pivot_histo.sum()
        data_plat_histo=data_plat_histo.set_index("fecha_hora")
        #st.line_chart(data=data_plat_histo)
        data_pivot_histo=data_pivot_histo.sort_index(ascending=False)
        data_pivot_histo["Total"]=0

        for fila in range(data_pivot_histo.shape[0]):
            for columna in range(data_pivot_histo.shape[1]-1):
                data_pivot_histo.iloc[fila,columna]=int(data_pivot_histo.iloc[fila,columna])
                data_pivot_histo.iloc[fila,data_pivot_histo.shape[1]-1]+=int(data_pivot_histo.iloc[fila,columna])

        
        datos_graficos=pd.DataFrame()
        if "Remoto" in data_pivot_histo.columns:
            if "Presencial" in data_pivot_histo.columns:
                datos_graficos["Ocupados"]=data_pivot_histo["Remoto"]+data_pivot_histo["Presencial"]
            else:
                datos_graficos["Ocupados"]=data_pivot_histo["Remoto"]
        else:
            if "Presencial" in data_pivot_histo.columns:
                datos_graficos["Ocupados"]=data_pivot_histo["Presencial"]
            else:
                datos_graficos["Ocupados"]=0
            
                
        
        datos_graficos["Libres"]=data_pivot_histo["Libres"]
        #st.dataframe(datos_graficos)
        st.line_chart(datos_graficos)





        st.dataframe(data_pivot_histo.head(200))


if informe=="Apagadas":
    st.text(f"Ultima actualizacion proceso PC: {fecha_proceso.iloc[0,0]} ({fecha_proceso.iloc[0,1]} minutos)")    
    st.text(f"Ultimo estado PCs              : {fecha_act.iloc[0,0]} ({fecha_act.iloc[0,1]} minutos)")

    data_apagadas=pd.read_sql('SELECT upper(Plataforma) as Plataforma, grupo, cantidad from s_apagadas_grupo_plataforma ', con)
    data_apagadas_sum=data_apagadas.cumsum()
    total_apagadas=data_apagadas_sum.tail(1)
    st.subheader(f"Total PCs apagadas: {str(total_apagadas.iloc[0,2])}")

    data_apagadas_plat=data_apagadas.groupby(by=["Plataforma"]).sum()
  

    st.dataframe(data_apagadas_plat.sort_values(by="cantidad", ascending=False))


    data_apagadas=data_apagadas.set_index(["Plataforma", "grupo"])
    st.dataframe(data=data_apagadas, width=450, height=1000)
    
    data_apagadas_so=pd.read_sql('SELECT grupo, soperativo, sum(cantidad) as cantidad from s_apagadas_grupo_plataforma group by grupo, soperativo order by 1,2', con)
    st.dataframe(data=data_apagadas_so, width=750, height=1000)
    
        
    data_apagadas_detalle=pd.read_sql('SELECT * from base_pcs where Estado="Off" and plataforma<>"VDI" and Red="Interna" order by UltimoEstado', con)
    # data_apagadas_detalle=data_apagadas_detalle.set_index("Ip")
    st.dataframe(data=data_apagadas_detalle, width=1200, height=400)
    
if informe=="Disponibles":
    tipo_vista_dispo=st.sidebar.radio("Vista", ['Fitro plataforma y estado', 'por Dias', 'Libres ahora', 'Listas para asignar', 'Sin stock disponible'])
    if tipo_vista_dispo=='Fitro plataforma y estado':
      
        data_plataformas=pd.read_sql('select distinct upper(plataforma) as plataforma from s_pc_disponibles_uso order by 1', con)
        tupla_plataformas=tuple(data_plataformas['plataforma'])
        #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
        plataforma_select_dispo=st.multiselect("Plataforma", tupla_plataformas)
          
           
        col1, col2 = st.beta_columns([3,3])
        with col1:
            modo_select_dispo=st.radio("Modo", ['Remoto', 'Presencial'])
        with col2:
            estado_select_dispo=st.radio("Estado", ['On', 'Off'])
          
        texto=""
        for i in range(len(plataforma_select_dispo)):
            texto+='"'
            texto+=plataforma_select_dispo[i]
            texto+='",'
        #st.text(texto)     
        
        if texto=="":
            st.subheader("Elegi al menos una plataforma")
        else:
            data_dispo=pd.read_sql('SELECT * from s_pc_disponibles_uso where upper(plataforma) in ('+texto+'"") and Modo="'+modo_select_dispo+'" and Estado="'+estado_select_dispo+'" order by ultimo_uso limit 25', con)
            st.table(data=data_dispo)
    if tipo_vista_dispo=='Sin stock disponible':
      
        data_imagen=pd.read_sql('select distinct upper(tipo_imagen) as tipo_imagen from s_q_sin_ip_dia_hora order by 1', con)
        tupla_imagen=tuple(data_imagen['tipo_imagen'])
        #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
        imagen_select_dispo=st.multiselect("Tipo Imagen", tupla_imagen)
          
           

        texto=""
        for i in range(len(imagen_select_dispo)):
            texto+='"'
            texto+=imagen_select_dispo[i]
            texto+='",'
        #st.text(texto)     
        
        if texto=="":
            st.subheader("Elegi al menos un tipo de imagen")
        else:
            data_dispo=pd.read_sql('SELECT * from s_q_sin_ip_dia_hora where upper(tipo_imagen) in ('+texto+'"") order by 1 desc limit 100', con)
            st.table(data=data_dispo)  
    if tipo_vista_dispo=='por Dias':
        #st.header("por dia")
        cantidad_dias_sin_uso=st.slider("dias sin uso", min_value=1, max_value=10, value=1, step=1)
        col1, col2 = st.beta_columns([3,3])
        with col1:
            modo_select_dias=st.radio("Modo", ['Remoto', 'Presencial'])
        with col2:
            estado_select_dias=st.radio("Estado", ['On', 'Off'])
                 
        
        data_dispo_dias=pd.read_sql('select upper(Plataforma) as plataforma, Estado, Modo, grupo, Soperativo, count(Ip) as cantidad from (select * from s_pc_disponibles_uso where Modo="'+modo_select_dias+'" and Estado="'+estado_select_dias+'" and ultimo_uso<date("now", "-'+str(cantidad_dias_sin_uso+1)+' days") union select * from s_pc_disponibles_uso where  Modo="'+modo_select_dias+'" and  Estado="'+estado_select_dias+'" and ultimo_uso is null ) a group by upper(Plataforma), Estado, Modo, grupo, Soperativo order by 6 desc,1,2,3,4,5 ', con)
        st.table(data_dispo_dias)


    if tipo_vista_dispo=='Libres ahora':
        data_libres_ahora=pd.read_sql('select * from s_libres', con)
        st.dataframe(data_libres_ahora, height=700)

        data_libres_detalle=pd.read_sql('select * from s_libres_detalle', con)
        st.dataframe(data_libres_detalle, height=700)

    if tipo_vista_dispo=='Listas para asignar':
        data_listas_ahora=pd.read_sql('select * from s_resumen_dispo_res', con)
        st.dataframe(data_listas_ahora, height=700)


if informe=="Cantidad por intervalo":
    data_resumen=pd.read_sql('SELECT * from s_region_mu', con)

    
    tipo_geografia=st.sidebar.selectbox('Geografia', tuple(data_resumen.TZ.unique()))       
    ahora=dt.datetime.now()
    fecha_informe=st.sidebar.date_input('Fecha', dt.date(ahora.year, ahora.month, ahora.day))
    # st.sidebar.text(fecha_informe)
    data_resumen_muid=data_resumen[data_resumen["TZ"]==tipo_geografia]
    tipo_muid=st.sidebar.selectbox('muid', tuple(data_resumen_muid.muID.unique())) 
    data_intervalos=pd.read_sql('SELECT * from s_cantidad_intervalo_exception where muId="'+str(tipo_muid)+'" and TZ="'+tipo_geografia+'" and fecha="'+str(fecha_informe)+'"', con)
    
    data_intervalo_pivot=data_intervalos.pivot(index='intervalo', columns='segmento', values='racs')
    data_intervalo_pivot=data_intervalo_pivot.fillna(0)
    # st.bar_chart(data_intervalo_pivot)
    data_intervalo_=data_intervalo_pivot.reset_index()
    
    fig1 = go.Figure()
    
    st.text (tipo_geografia+"  " + str(tipo_muid)+ "   " + str(fecha_informe))
    
    k=0
    for column in data_intervalo_:
        if k==0:
            pass
        else:
            fig1.add_trace(go.Scatter(x=data_intervalo_["intervalo"], y=data_intervalo_[column],line=dict(color=colores[k], width=2),name=column))
            
        k+=1
    


    fig1.update_xaxes(type='category')
    fig1.update_layout(height=450, width=1200)
    st.plotly_chart(fig1, use_container_width=True)


    st.table(data=data_intervalo_pivot)
    
    # if tipo_info=='Resumen':
    #     data_nousan_group=data_nousan.drop(columns=['UsuarioConectado', 'cliente','PROGRAMA','fecha', 'ip_login', 'ip_asignada'])
                 
    #     data_nousan_group=data_nousan_group.groupby(by=["NOMBRE_GERENTE", "NOMBRE_JEFATURA","NOMBRE_RESPONSABLE_SUPERVISOR"]).count()

    #     st.table(data=data_nousan_group.sort_values(by=['NOMBRE_PERSONAL'], ascending=False))
        
    # if tipo_info=='Gerente':
    #     tupla_gerentes=tuple(data_nousan.NOMBRE_GERENTE.unique())
    #     #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
    #     gerente_select=st.sidebar.radio("Gerente", tupla_gerentes)
    #     st.table(data=data_nousan[(data_nousan.NOMBRE_GERENTE==gerente_select) ] ) 

    # if tipo_info=='Jefe':
    #     tupla_jefes=tuple(data_nousan.NOMBRE_JEFATURA.unique())
    #     #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
    #     jefe_select=st.sidebar.radio("Jefe", sorted(tupla_jefes))
        
    #     st.table(data=data_nousan[ (data_nousan.NOMBRE_JEFATURA==jefe_select)] ) 
 
    # if tipo_info=='Supervisor':
    #     tupla_supervisores=tuple(data_nousan.NOMBRE_RESPONSABLE_SUPERVISOR.unique())
    #     #plataforma_select=st.sidebar.selectbox("Plataforma",tupla_plataformas)
    #     supervisor_select=st.sidebar.radio("Supervisor", sorted(tupla_supervisores))
        
    #     st.table(data=data_nousan[ (data_nousan.NOMBRE_RESPONSABLE_SUPERVISOR==supervisor_select)] ) 
 