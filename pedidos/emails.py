from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def enviar_correo_pedido(pedido):
    """
    Envía el correo de confirmación del pedido.

    Funciona tanto para:
    - Usuarios registrados.
    - Usuarios invitados.
    """

    destinatario = pedido.correo_comprador

    if not destinatario:
        return

    # ============================================================
    # INFORMACIÓN DEL PEDIDO
    # ============================================================

    numero_pedido = pedido.id

    nombre = pedido.nombre_comprador
    apellido = pedido.apellido_comprador

    estado = pedido.get_estado_display()

    fecha = pedido.fecha_creacion.strftime(
        "%d/%m/%Y %H:%M"
    )

    # ============================================================
    # DIRECCIÓN
    # ============================================================

    direccion = pedido.nombre_direccion

    calle = pedido.calle
    numero = pedido.numero
    comuna = pedido.comuna
    region = pedido.region
    informacion_adicional = (
        pedido.informacion_adicional
    )

    # ============================================================
    # PRODUCTOS
    # ============================================================

    detalles = pedido.detalles.all()

    productos_html = ""

    for detalle in detalles:

        precio_unitario = (
            f"${detalle.precio_unitario:,.0f}"
            .replace(",", ".")
        )

        subtotal = (
            f"${detalle.subtotal:,.0f}"
            .replace(",", ".")
        )

        productos_html += f"""
        <tr>
            <td style="
                padding: 12px;
                border-bottom: 1px solid #eeeeee;
            ">
                {detalle.nombre_producto}
            </td>

            <td style="
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #eeeeee;
            ">
                {detalle.cantidad}
            </td>

            <td style="
                padding: 12px;
                text-align: right;
                border-bottom: 1px solid #eeeeee;
            ">
                {precio_unitario}
            </td>

            <td style="
                padding: 12px;
                text-align: right;
                border-bottom: 1px solid #eeeeee;
                font-weight: bold;
            ">
                {subtotal}
            </td>
        </tr>
        """

    # ============================================================
    # VALORES
    # ============================================================

    subtotal = (
        f"${pedido.subtotal:,.0f}"
        .replace(",", ".")
    )

    costo_despacho = (
        f"${pedido.costo_despacho:,.0f}"
        .replace(",", ".")
    )

    total = (
        f"${pedido.total:,.0f}"
        .replace(",", ".")
    )

    # ============================================================
    # ASUNTO
    # ============================================================

    asunto = (
        f"Pedido #{numero_pedido} confirmado - HogarExpress"
    )

    # ============================================================
    # MENSAJE DE TEXTO
    # ============================================================

    mensaje_texto = f"""
Hola {nombre} {apellido},

¡Gracias por comprar en HogarExpress!

Tu pedido #{numero_pedido} fue realizado correctamente.

Estado: {estado}
Fecha: {fecha}

TOTAL: {total}

Dirección de despacho:
{calle} {numero}
{comuna}, {region}

Este correo contiene el comprobante de tu compra.

Gracias por confiar en HogarExpress.
"""

    # ============================================================
    # MENSAJE HTML
    # ============================================================

    mensaje_html = f"""
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>
        Pedido #{numero_pedido}
    </title>

</head>

<body style="
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
    font-family: Arial, Helvetica, sans-serif;
">

    <div style="
        max-width: 700px;
        margin: 30px auto;
        background-color: #ffffff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    ">

        <!-- ================================================= -->
        <!-- ENCABEZADO -->
        <!-- ================================================= -->

        <div style="
            background-color: #15803d;
            padding: 30px;
            text-align: center;
            color: white;
        ">

            <h1 style="
                margin: 0;
                font-size: 28px;
            ">
                HogarExpress
            </h1>

            <p style="
                margin: 8px 0 0;
                font-size: 16px;
            ">
                Confirmación de compra
            </p>

        </div>


        <!-- ================================================= -->
        <!-- CONTENIDO -->
        <!-- ================================================= -->

        <div style="
            padding: 30px;
        ">

            <h2 style="
                color: #222222;
                margin-top: 0;
            ">
                ¡Gracias por tu compra!
            </h2>

            <p style="
                color: #555555;
                line-height: 1.6;
            ">
                Hola <strong>{nombre} {apellido}</strong>,
            </p>

            <p style="
                color: #555555;
                line-height: 1.6;
            ">
                Hemos recibido correctamente tu pedido.
                A continuación encontrarás toda la
                información de tu compra.
            </p>


            <!-- ================================================= -->
            <!-- PEDIDO -->
            <!-- ================================================= -->

            <div style="
                background-color: #f0fdf4;
                border-radius: 10px;
                padding: 20px;
                margin-top: 25px;
            ">

                <p style="
                    margin: 0 0 8px;
                    color: #666666;
                ">
                    Número de pedido
                </p>

                <p style="
                    margin: 0;
                    font-size: 24px;
                    font-weight: bold;
                    color: #15803d;
                ">
                    #{numero_pedido}
                </p>

                <p style="
                    margin: 15px 0 0;
                    color: #555555;
                ">
                    <strong>Estado:</strong>
                    {estado}
                </p>

                <p style="
                    margin: 8px 0 0;
                    color: #555555;
                ">
                    <strong>Fecha:</strong>
                    {fecha}
                </p>

            </div>


            <!-- ================================================= -->
            <!-- PRODUCTOS -->
            <!-- ================================================= -->

            <h2 style="
                margin-top: 30px;
                color: #222222;
                font-size: 20px;
            ">
                Productos de tu pedido
            </h2>

            <table style="
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            ">

                <thead>

                    <tr style="
                        background-color: #f5f5f5;
                    ">

                        <th style="
                            padding: 12px;
                            text-align: left;
                        ">
                            Producto
                        </th>

                        <th style="
                            padding: 12px;
                            text-align: center;
                        ">
                            Cant.
                        </th>

                        <th style="
                            padding: 12px;
                            text-align: right;
                        ">
                            Precio
                        </th>

                        <th style="
                            padding: 12px;
                            text-align: right;
                        ">
                            Subtotal
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {productos_html}

                </tbody>

            </table>


            <!-- ================================================= -->
            <!-- RESUMEN -->
            <!-- ================================================= -->

            <div style="
                margin-top: 25px;
                border-top: 1px solid #eeeeee;
                padding-top: 20px;
            ">

                <div style="
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 10px;
                    color: #555555;
                ">

                    <span>
                        Subtotal
                    </span>

                    <strong>
                        {subtotal}
                    </strong>

                </div>

                <div style="
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 15px;
                    color: #555555;
                ">

                    <span>
                        Despacho
                    </span>

                    <strong>
                        {costo_despacho}
                    </strong>

                </div>

                <div style="
                    border-top: 2px solid #eeeeee;
                    padding-top: 15px;
                    display: flex;
                    justify-content: space-between;
                ">

                    <span style="
                        font-size: 20px;
                        font-weight: bold;
                    ">
                        Total
                    </span>

                    <span style="
                        font-size: 24px;
                        font-weight: bold;
                        color: #15803d;
                    ">
                        {total}
                    </span>

                </div>

            </div>


            <!-- ================================================= -->
            <!-- DIRECCIÓN -->
            <!-- ================================================= -->

            <h2 style="
                margin-top: 35px;
                color: #222222;
                font-size: 20px;
            ">
                Dirección de despacho
            </h2>

            <div style="
                background-color: #f8fafc;
                border-radius: 10px;
                padding: 20px;
                color: #555555;
                line-height: 1.6;
            ">

                <strong>
                    {direccion}
                </strong>

                <br>

                {calle} {numero}

                <br>

                {comuna}, {region}

                {
                    f"<br><br>{informacion_adicional}"
                    if informacion_adicional
                    else ""
                }

            </div>


            <!-- ================================================= -->
            <!-- PAGO -->
            <!-- ================================================= -->

            <div style="
                margin-top: 25px;
                background-color: #f0fdf4;
                border-radius: 10px;
                padding: 18px;
                color: #166534;
            ">

                <strong>
                    ✓ Pago confirmado
                </strong>

            </div>


            <!-- ================================================= -->
            <!-- FINAL -->
            <!-- ================================================= -->

            <p style="
                margin-top: 30px;
                color: #555555;
                line-height: 1.6;
            ">
                Guarda este correo como comprobante de tu
                compra. También podrás utilizar el número
                de pedido <strong>#{numero_pedido}</strong>
                para futuras consultas.
            </p>

            <p style="
                color: #555555;
                line-height: 1.6;
            ">
                Gracias por confiar en
                <strong>HogarExpress</strong>.
            </p>

        </div>


        <!-- ================================================= -->
        <!-- PIE -->
        <!-- ================================================= -->

        <div style="
            background-color: #f8fafc;
            padding: 20px;
            text-align: center;
            color: #888888;
            font-size: 13px;
        ">

            <p style="margin: 0;">
                HogarExpress
            </p>

            <p style="
                margin: 6px 0 0;
            ">
                Este correo fue generado automáticamente.
            </p>

        </div>

    </div>

</body>

</html>
"""

    # ============================================================
    # CREAR Y ENVIAR CORREO
    # ============================================================

    email = EmailMultiAlternatives(
        subject=asunto,
        body=mensaje_texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )

    email.attach_alternative(
        mensaje_html,
        "text/html"
    )

    email.send(fail_silently=False)
