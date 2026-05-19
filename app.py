#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluación 2 - Consumo de API Deportiva (TheSportsDB)
VERSION MEJORADA - Extrae máximos campos posibles de forma automática
"""

import os
import sys
import json
import requests
from datetime import datetime

API_BASE = "https://www.thesportsdb.com/api/v1/json/3"
API_KEY = os.getenv("SPORTSDB_KEY", "sin_clave_requerida")

def print_separator():
    print("=" * 60)

def main():
    print_separator()
    print("🏆 EVALUACIÓN 2 - CONSULTA API DEPORTIVA (TheSportsDB)")
    print(f"📅 Fecha y hora: {datetime.now()}")
    print(f"🔑 API Key configurada: {API_KEY[:10]}..." if API_KEY != "sin_clave_requerida" else "🔑 Sin API Key requerida")
    print_separator()

    # ========== PASO 1: LIGAS ==========
    print("\n📡 1. Consultando ligas de fútbol...")
    try:
        response = requests.get(f"{API_BASE}/all_leagues.php", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("   ✅ Conexión exitosa")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)

    leagues = data.get("leagues", [])
    soccer_leagues = [l for l in leagues if l.get("strSport") == "Soccer" and l.get("strLeague")]

    if not soccer_leagues:
        print("   ❌ No se encontraron ligas")
        sys.exit(1)

    # Selección automática de la primera liga
    selected = soccer_leagues[0]
    league_name = selected.get('strLeague', 'N/A')
    league_id = selected.get('idLeague')
    
    print(f"\n🏆 LIGA SELECCIONADA:")
    print(f"   • Nombre: {league_name}")
    print(f"   • País: {selected.get('strCountry', 'N/A')}")
    print(f"   • Deporte: {selected.get('strSport', 'N/A')}")
    print(f"   • Alternativo: {selected.get('strLeagueAlternate', 'N/A')}")
    print(f"   • ID Liga: {league_id if league_id else 'N/A'}")

    # ========== PASO 2: EQUIPOS ==========
    print(f"\n📋 2. Consultando equipos de {league_name}...")
    teams = []
    
    if league_id:
        url = f"{API_BASE}/lookup_all_teams.php?id={league_id}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200 and resp.text:
                teams_data = resp.json()
                teams = teams_data.get("teams", [])
        except:
            pass
    
    if not teams:
        url = f"{API_BASE}/search_all_teams.php?l={league_name.replace(' ', '%20')}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200 and resp.text:
                teams_data = resp.json()
                teams = teams_data.get("teams", [])
        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    if teams:
        print(f"   ✅ {len(teams)} equipos encontrados. Mostrando 3:\n")
        for i, t in enumerate(teams[:3], 1):
            print(f"   {i}. {t.get('strTeam', 'N/A')}")
            print(f"      • Estadio: {t.get('strStadium', 'N/A')}")
            print(f"      • Fundado: {t.get('intFormedYear', 'N/A')}")
            print(f"      • Ciudad: {t.get('strLocation', 'N/A')}")
            print(f"      • Capacidad: {t.get('intStadiumCapacity', 'N/A')}")
            print()
    else:
        print("   ⚠️ No se encontraron equipos")
        teams = []

    # ========== PASO 3: JUGADOR ==========
    print("⚽ 3. Jugador representativo...")
    
    famous_players = ["Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappe", "Kevin De Bruyne", "Erling Haaland"]
    player_found = False
    
    if teams and len(teams) > 0:
        first_team = teams[0]
        team_id = first_team.get('idTeam')
        team_name = first_team.get('strTeam')
        
        if team_id:
            url = f"{API_BASE}/lookup_all_players.php?id={team_id}"
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200 and resp.text:
                    players_data = resp.json()
                    players = players_data.get("player", [])
                    if players and len(players) > 0:
                        p = players[0]
                        print(f"   🎮 {p.get('strPlayer', 'N/A')} (de {team_name})")
                        print(f"      • Nacionalidad: {p.get('strNationality', 'N/A')}")
                        print(f"      • Posición: {p.get('strPosition', 'N/A')}")
                        print(f"      • Dorsal: {p.get('strNumber', 'N/A')}")
                        print(f"      • Nacimiento: {p.get('dateBorn', 'N/A')}")
                        print(f"      • Altura: {p.get('strHeight', 'N/A')}")
                        print(f"      • Peso: {p.get('strWeight', 'N/A')}")
                        player_found = True
            except:
                pass
    
    if not player_found:
        print("   🔍 Buscando jugador destacado global...")
        for player_name in famous_players:
            try:
                url = f"{API_BASE}/searchplayers.php?p={player_name.replace(' ', '%20')}"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200 and resp.text:
                    players_data = resp.json()
                    players = players_data.get("player", [])
                    if players and len(players) > 0:
                        p = players[0]
                        print(f"   🎮 {p.get('strPlayer', 'N/A')} (Referencia global)")
                        print(f"      • Nacionalidad: {p.get('strNationality', 'N/A')}")
                        print(f"      • Posición: {p.get('strPosition', 'N/A')}")
                        print(f"      • Dorsal: {p.get('strNumber', 'N/A')}")
                        print(f"      • Nacimiento: {p.get('dateBorn', 'N/A')}")
                        print(f"      • Altura: {p.get('strHeight', 'N/A')}")
                        print(f"      • Peso: {p.get('strWeight', 'N/A')}")
                        player_found = True
                        break
            except:
                continue
    
    if not player_found:
        print("   ⚠️ No se pudo obtener información de jugadores")

    # ========== PASO 4: RESUMEN FINAL ==========
    print_separator()
    print("✅ CONSULTA FINALIZADA CON ÉXITO")
    print(f"📊 RESUMEN DE DATOS EXTRAÍDOS:")
    print(f"   • Ligas de fútbol disponibles: {len(soccer_leagues)}")
    print(f"   • Liga seleccionada: {league_name}")
    print(f"   • Equipos encontrados: {len(teams) if teams else 0}")
    print(f"   • Campos por equipo: 5 (nombre, estadio, fundación, ciudad, capacidad)")
    print(f"   • Estado: Consulta completada")
    print_separator()
    sys.exit(0)

if __name__ == "__main__":
    main()