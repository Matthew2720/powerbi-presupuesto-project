let
    Source = Csv.Document(File.Contents("c:\\Users\\USER\\Desktop\\Prueba\\Prueba de Excel y BI - Asesor de Area Empleo.csv"), [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Trimmed" = Table.TransformColumns(#"Promoted Headers", {{"Mes", each Text.Trim(_), type text}, {"Tipo de gasto", each Text.Trim(_), type text}, {"Importe en moneda local", each Text.Trim(Text.Replace(_, Character.FromNumber(160), " ")), type text}, {"Fe.contabilización", each Text.Trim(_), type text}, {"Equipo", each Text.Trim(_), type text}}),
    #"Parsed Date" = Table.TransformColumns(#"Trimmed", {{"Fe.contabilización", each Date.FromText(_, "es-ES"), type date}}),
    Meses = {"Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"},
    #"Added MesNumero" = Table.AddColumn(#"Parsed Date", "MesNumero", each let pos = List.PositionOf(Meses, [Mes]) in if pos = -1 then null else pos + 1, Int64.Type),
    #"Added Año" = Table.AddColumn(#"Added MesNumero", "Año", each Date.Year([Fe.contabilización]), Int64.Type),
    CleanMoney = (t as text) as number => let neg = Text.Contains(t, "-"), digits = Text.Select(t, {"0".."9"}), n = if digits = "" then 0 else Number.From(digits) in if neg then -n else n,
    #"Added Monto Ejecutado" = Table.AddColumn(#"Added Año", "Monto Ejecutado", each CleanMoney([Importe en moneda local]), type number),
    #"Selected Columns" = Table.SelectColumns(#"Added Monto Ejecutado", {"Tipo de gasto", "Mes", "MesNumero", "Año", "Equipo", "Fe.contabilización", "Monto Ejecutado"}),
    #"Added Periodo" = Table.AddColumn(#"Selected Columns", "Periodo", each #date([Año],[MesNumero],1), type date)
in
    #"Added Periodo"