🎓 CONTEXTO — Módulo de Criptografia (Cibersegurança, MEEC)

Estou a criar decks de slides para o módulo de Criptografia, dentro da UC de Cibersegurança do Mestrado em Engenharia Eletrotécnica e de Computadores. Cada deck corresponde a um capítulo da sebenta (ver estrutura do módulo, abaixo — 11 capítulos, ainda que leccionados em 10 aulas). Usa sempre as seguintes convenções de estilo e layout. Cada deck deve ter entre 20 e 25 slides, nunca excedendo os 30. Os slides devem estar preparados para exportar para o PowerPoint, pelo que não quero slides "compridos" que não permitam uma exportação para o power point.

Vou-te passar as instruções de construção dos slides aqui neste texto, depois deves perguntar-me pelo texto do capítulo e eu copio e colo (ou passo-te um ficheiro). Antes de começares deves perguntar se há figuras a inserir. Se houver eu insiro e tu deves conservar o mais possível as que forem diagramas e não as substituir por imagens generativas. No entanto podes e deves melhorá-las esteticamente e usar a paleta de cores do resto do esquema dos slides. Deverás inserir essas figuras nos locais indicados nos ficheiros de texto.

Todos os termos em inglês nos slides de língua portuguesa devem ser italicizados. Excetua-se código (Python, etc.) e nomes próprios de algoritmos/protocolos/normas (AES, RSA, SHA-256, TLS, PGP, X.509, etc.), que não se italicizam.

🎨 TEMAS POR BLOCO

Todos os temas abaixo têm de ser **light** — nunca escolher um tema dark, mesmo que pareça combinar bem com a cor do bloco.

Apresentação: tema Pearl ou Howlite
Capítulo 1 (Bloco 1 — Criptografia Clássica): tema Rush ou Ashrose
Capítulos 2–4 (Bloco 2 — Criptografia Simétrica Moderna): tema Rush ou Icebreaker
Capítulo 5 (Bloco 3 — Integridade e Autenticação): tema Ash ou Chimney Smoke
Capítulos 6–8 (Bloco 4 — Criptografia Assimétrica): tema Consultant ou Gold Leaf
Capítulos 9–11 (Bloco 5 — Infraestrutura e Aplicações): tema Rush ou Zephyr

🖼️ IMAGENS ILUSTRATIVAS

Estilo: isometric illustration, clean geometric shapes, flat colors, technical/security aesthetic, [cor do bloco] and white palette, no shadows, crisp lines
Modelo: ideogram-v4-turbo (verificar se continua disponível antes de cada novo deck)
Formato preferido: quadrado (square) para imagens em colunas; portrait para accent images laterais
artStylePreset: custom (verificar se continua um parâmetro válido antes de cada novo deck)

📐 DIAGRAMAS E ESQUEMAS TÉCNICOS

Fundo branco, tipografia limpa, sem gradientes
Cor de destaque: carmesim (#b0202a ou similar) para o Bloco 1; adaptar à cor do bloco nos outros decks
Melhorar diagramas existentes com gpt-image-2-mini (imageEditContent), mantendo estrutura e substituindo apenas as cores
Exemplos de diagramas por bloco: Modelo de Cifra Simétrica, Grelha de Playfair, Grelha de Transposição Colunar (Bloco 1); Rede de Feistel, Estágios do AES, Modos de Operação (Bloco 2); Propriedades de uma Função de Hash, Mecanismo HMAC (Bloco 3); Confidencialidade vs. Autenticação com Par de Chaves, Troca Diffie-Hellman, Curva Elíptica (Bloco 4); Cadeia de Certificação X.509, Handshake TLS 1.3, Cifra Híbrida PGP (Bloco 5)

👥 PERSONAGENS RECORRENTES

Não aplicável a este módulo — sem projeto-fio-condutor nem personagens fixos.

📄 LAYOUT DOS SLIDES

O primeiro slide terá que ter obrigatóriamente uma imagem que "resuma" o tema do deck. Essa imagem será inserida no slide 1; para além disso deve ser feita uma segunda cópia dessa imagem no formato 16:9 e colocada na pasta de média.
Título (h1) e label fora e acima das colunas
Imagem numa coluna (40–45%), texto na outra (55–60%)
Imagens com dimensions="fill" para preencher a coluna
Accent image lateral (image-layout="left" ou "right") para slides mais simples com uma única imagem
Label variant="solid" para slides de conteúdo; variant="outline" para slides de capa/abertura

💾 COMPATIBILIDADE POWERPOINT

Evitar smart layouts complexos (arrows, processSteps) — substituir por listas numeradas em <p> com bold
Smart layouts simples (outlineBoxesWithSideLine, bigBullets, solidBoxes) são aceitáveis
Imagens em colunas exportam bem; accent images também

🌍 LÍNGUA

Todo o conteúdo em Português europeu (pt-PT)
Responde-me sempre em português

📚 ESTRUTURA DO MÓDULO (para referência)

O módulo tem 10 aulas teóricas, mas a sebenta e os decks de slides organizam-se por 11 capítulos — as duas últimas aulas de conteúdo (Capítulos 10 e 11) são leccionadas na mesma sessão.

Apresentação (fora da distribuição de conteúdo, sem número de capítulo)
Bloco 1 — Criptografia Clássica: Capítulo 1 (substituição, transposição, César, monoalfabética, Playfair, Vigenère, One-Time Pad)
Bloco 2 — Criptografia Simétrica Moderna: Capítulo 2 (Cifras de Bloco — Feistel, DES/3DES), Capítulo 3 (AES), Capítulo 4 (Cifras de Fluxo — RC4, Salsa20, ChaCha20)
Bloco 3 — Integridade e Autenticação: Capítulo 5 (Hashing, SHA, MAC, HMAC)
Bloco 4 — Criptografia Assimétrica: Capítulo 6 (Fundamentos, RSA), Capítulo 7 (Diffie-Hellman, Assinaturas Digitais), Capítulo 8 (Curva Elíptica — ECC)
Bloco 5 — Infraestrutura e Aplicações: Capítulo 9 (PKI, certificados X.509, MITM), Capítulo 10 (TLS, PGP), Capítulo 11 (Eficiência Algorítmica e Criptografia Pós-Quântica — leccionado na mesma aula que o Capítulo 10)
