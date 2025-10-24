let
    Source = Csv.Document(File.Contents("c:\\Users\\USER\\Desktop\\Prueba\\presupuesto2.csv"), [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Removed Total" = Table.SelectRows(#"Promoted Headers", each not Text.Contains(Text.Lower(Text.From([Proyección])), "total")),
    Meses = {"Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"},
    #"Unpivoted Months" = Table.UnpivotOtherColumns(#"Removed Total", {"Proyección"}, "Mes", "MontoTexto"),
    #"Trimmed" = Table.TransformColumns(#"Unpivoted Months", {{"Mes", each Text.Trim(_), type text}, {"Proyección", each Text.Trim(_), type text}, {"MontoTexto", each Text.Trim(Text.Replace(_, Character.FromNumber(160), " ")), type text}}),
    CleanMoney = (t as text) as number => let neg = Text.Contains(t, "-"), digits = Text.Select(t, {"0".."9"}), n = if digits = "" then 0 else Number.From(digits) in if neg then -n else n,
    #"Added Equipo" = Table.AddColumn(#"Trimmed", "Equipo", each "Equipo 2", type text),
    #"Added Año" = Table.AddColumn(#"Added Equipo", "Año", each 2023, Int64.Type),
    #"Added MesNumero" = Table.AddColumn(#"Added Año", "MesNumero", each let pos = List.PositionOf(Meses, [Mes]) in if pos = -1 then null else pos + 1, Int64.Type),
    #"Renamed Columns" = Table.RenameColumns(#"Added MesNumero", {{"Proyección", "Tipo de gasto"}}),
    #"Added Monto Presupuestado" = Table.AddColumn(#"Renamed Columns", "Monto Presupuestado", each CleanMoney([MontoTexto]), type number),
    #"Removed Columns" = Table.RemoveColumns(#"Added Monto Presupuestado", {"MontoTexto"}),
    #"Added Periodo" = Table.AddColumn(#"Removed Columns", "Periodo", each #date([Año],[MesNumero],1), type date)
in
    #"Added Periodo"