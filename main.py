import flet as ft
import aiohttp
import asyncio

pokemon_actual = 0

async def main(page: ft.Page):
    # New window dimensions
    new_window_width = 400
    new_window_height = 850

    # Calculate scaling factors
    width_scale_factor = new_window_width / 720
    height_scale_factor = new_window_height / 1280

    page.window_width = new_window_width
    page.window_height = new_window_height
    page.window_resizable = False
    page.padding = 0
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf",
    }
    page.theme = ft.Theme(font_family="zpix")

    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_pokemon(e: ft.ContainerTapEvent):
        global pokemon_actual

        if e.control == flecha_superior:
            pokemon_actual += 1
        else:
            pokemon_actual -= 1

        numero = (pokemon_actual % 150) + 1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")

        datos = f"Nombre: {resultado['name']}\n\nAbilidades:\n"
        for elemento in resultado["abilities"]:
            habilidad = elemento["ability"]["name"]
            datos += f"\n{habilidad}"
        datos += f"\n\nPeso: {resultado['height']} kg"
        texto.value = datos
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url

        await page.update_async()

    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.CYAN_100
            await page.update_async()
            await asyncio.sleep(0.1)
            await page.update_async()
            luz_azul.bgcolor = ft.colors.CYAN
            await page.update_async()

    # Container dimensions scaling
    container_width = int(600 * width_scale_factor)
    container_height = int(400 * height_scale_factor)

    luz_azul = ft.Container(width=35, height=35, left=23, top=12, bgcolor=ft.colors.CYAN, border_radius=50)

    boton_azul = ft.Stack([
        ft.Container(width=40, height=40, bgcolor=ft.colors.WHITE, border_radius=50, left=20, top=10),
        luz_azul,
    ])

    items_superior = [
        ft.Container(boton_azul, width=80, height=80),
        ft.Container(width=int(40 * width_scale_factor), height=int(40 * height_scale_factor-5),
                     bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=int(40 * width_scale_factor), height=int(40 * height_scale_factor-5),
                     bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=int(40 * width_scale_factor), height=int(40 * height_scale_factor-5),
                     bgcolor=ft.colors.GREEN, border_radius=50)
    ]

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    # Image dimensions scaling
    image_width = int(30 * width_scale_factor)
    image_height = int(30 * height_scale_factor)

    imagen = ft.Image(
        src=sprite_url,
        scale=15,
        width=image_width,
        height=image_height,
        top=125,
        right=150,
    )

    stack_central = ft.Stack([
        ft.Container(width=container_width, height=container_height, bgcolor=ft.colors.WHITE, border_radius=20),
        ft.Container(width=int(550 * width_scale_factor), height=int(350 * height_scale_factor),
                     bgcolor=ft.colors.BLACK, top=15, left=15),
        imagen,
    ])

    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(20, 0),
            ft.canvas.Path.LineTo(0, 30),
            ft.canvas.Path.LineTo(40, 30),
        ],
            paint=ft.Paint(
                style=ft.PaintingStyle.FILL,
            )
        ),
    ],
        width=int(40 * width_scale_factor),
        height=int(30 * height_scale_factor)
    )

    flecha_superior = ft.Container(triangulo, width=int(160 * width_scale_factor),
                                   height=int(50 * height_scale_factor), on_click=get_pokemon)

    flechas = ft.Column([
        flecha_superior,
        ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159), width=int(160 * width_scale_factor)-48,
                     height=int(50 * height_scale_factor), on_click=get_pokemon),
    ]
    )

    texto = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=int(22 * height_scale_factor)
    )

    items_inferior = [
        ft.Container(width=int(20 * width_scale_factor)),  # Margen Izquierdo
        ft.Container(texto, padding=int(10 * width_scale_factor), width=int(400 * width_scale_factor),
                     height=int(300 * height_scale_factor), bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(width=int(30 * width_scale_factor)),  # Margen Derecho
        ft.Container(flechas, width=int(80 * width_scale_factor), height=int(120 * height_scale_factor)),
    ]

    superior = ft.Container(content=ft.Row(items_superior), width=container_width, height=int(80 * height_scale_factor),
                            margin=ft.margin.only(top=int(40 * height_scale_factor)))
    centro = ft.Container(content=stack_central, width=container_width, height=container_height,
                          margin=ft.margin.only(top=int(40 * height_scale_factor)),
                          alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=container_width, height=container_height,
                            margin=ft.margin.only(top=int(40 * height_scale_factor)))

    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior
    ]
    )

    contenedor = ft.Container(col, width=new_window_width, height=new_window_height, bgcolor=ft.colors.RED_700,
                              alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await blink()

ft.app(target=main)
