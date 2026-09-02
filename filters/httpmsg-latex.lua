-- Converte divs `::: {.httpmsg}` (e outras classes registadas em
-- LATEX_ENV_DIVS) em ambientes LaTeX \begin{...}\end{...} do mesmo
-- nome, ao gerar PDF. Em HTML não faz nada — a caixa já funciona via
-- CSS (div.httpmsg em custom.css). Sem este filtro, o pandoc ignora
-- silenciosamente a classe da div ao escrever LaTeX.

local LATEX_ENV_DIVS = { httpmsg = true }

function Div(el)
  if not quarto.doc.is_format("pdf") then
    return el
  end
  for _, class in ipairs(el.classes) do
    if LATEX_ENV_DIVS[class] then
      table.insert(el.content, 1, pandoc.RawBlock("latex", "\\begin{" .. class .. "}"))
      table.insert(el.content, pandoc.RawBlock("latex", "\\end{" .. class .. "}"))
      return el
    end
  end
end
