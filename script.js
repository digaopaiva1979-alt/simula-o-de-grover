document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // HAMBURGER MENU TOGGLE
    // =========================
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking on a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navToggle.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    // =========================
    // TYPEWRITER EFFECT (OTIMIZADO)
    // =========================
    const el = document.querySelector(".typewriter");

    const texts = [
        "Perito Judicial com atuação no TJSP e suporte técnico em litígios complexos",
        "Especialista em Computação Forense e reconstrução de evidências digitais",
        "Atuação avançada em Segurança Cibernética e resposta a incidentes",
        "Análise de Cadeia de Custódia com conformidade legal e integridade probatória",
        "Investigação de logs, correlação de eventos e rastreabilidade digital",
        "Produção de laudos técnicos com validade jurídica e rigor metodológico",
        "Atuação em perícia digital aplicada a fraudes, vazamentos e crimes cibernéticos",
        "Pesquisa aplicada em tecnologias emergentes e computação quântica",
        "Análise forense em dispositivos, redes e ambientes corporativos",
        "Suporte técnico para advogados em estratégias probatórias digitais"
    ];

    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingTimeout = null;

    function typeEffect() {
        if (!el) return;

        const currentText = texts[textIndex];
        
        if (isDeleting) {
            // Apagando caracteres
            if (charIndex > 0) {
                el.innerHTML = currentText.substring(0, charIndex - 1);
                charIndex--;
                typingTimeout = setTimeout(typeEffect, 30); // Apagar mais rápido
            } else {
                // Terminou de apagar, vai para próximo texto
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typingTimeout = setTimeout(typeEffect, 300);
            }
        } else {
            // Digitando caracteres
            if (charIndex < currentText.length) {
                el.innerHTML = currentText.substring(0, charIndex + 1);
                charIndex++;
                typingTimeout = setTimeout(typeEffect, 45); // Velocidade de digitação
            } else {
                // Terminou de digitar, pausa antes de apagar
                isDeleting = true;
                typingTimeout = setTimeout(typeEffect, 2500); // Pausa maior ao final
            }
        }
    }

    if (el) {
        // Iniciar com texto vazio
        el.innerHTML = "";
        typeEffect();
    }

    // Cleanup timeouts on page unload
    window.addEventListener('beforeunload', function() {
        if (typingTimeout) clearTimeout(typingTimeout);
    });

    // =========================
    // SWIPER CARROSSEL (MAIS RÁPIDO)
    // =========================
    if (typeof Swiper !== "undefined") {
        const swiper = new Swiper(".image-swiper", {
            loop: true,
            autoplay: {
                delay: 2500,              // Troca a cada 2.5 segundos (mais rápido)
                disableOnInteraction: false,
                pauseOnMouseEnter: false  // Não pausa ao passar mouse
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
                dynamicBullets: true      // Balas dinâmicas mais modernas
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev"
            },
            spaceBetween: 25,
            slidesPerView: 1,
            speed: 400,                   // Velocidade de transição mais rápida (antes 800)
            grabCursor: true,
            effect: 'slide',              // Efeito deslizante suave
            touchRatio: 1,
            resistanceRatio: 0.85,
            
            // Breakpoints responsivos
            breakpoints: {
                0: {
                    slidesPerView: 1,
                    spaceBetween: 15
                },
                640: { 
                    slidesPerView: 2, 
                    spaceBetween: 20,
                    speed: 350
                },
                1024: { 
                    slidesPerView: 3, 
                    spaceBetween: 25,
                    speed: 400
                }
            },
            
            // Melhorias de performance
            lazy: {
                loadPrevNext: true,
                loadPrevNextAmount: 1
            },
            
            // Keyboard navigation
            keyboard: {
                enabled: true,
                onlyInViewport: true
            }
        });
        
        // Pausar autoplay em hover (opcional - descomente se quiser)
        // const swiperContainer = document.querySelector(".image-swiper");
        // if (swiperContainer) {
        //     swiperContainer.addEventListener("mouseenter", () => swiper.autoplay.stop());
        //     swiperContainer.addEventListener("mouseleave", () => swiper.autoplay.start());
        // }
        
        console.log("Swiper inicializado com velocidade rápida");
    } else {
        console.warn("Swiper não carregado");
    }

    // =========================
    // CANVAS MATRIX EFFECT (OTIMIZADO - MARCA D'ÁGUA DIGITAL)
    // =========================
    const canvas = document.getElementById("bg-canvas");
    const ctx = canvas ? canvas.getContext("2d") : null;

    const binaryChars = "01";
    const fontSize = 14;
    let columns = 0;
    let drops = [];
    let animationFrameId = null;
    let lastTimestamp = 0;
    const frameInterval = 80; // 80ms entre frames (performance otimizada - ligeiramente mais rápida)

    function resizeCanvas() {
        if (!canvas) return;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function initDrops() {
        if (!canvas) return;
        columns = Math.floor(canvas.width / fontSize);
        drops = Array(columns).fill(1);
    }

    function drawMatrix(now) {
        if (!ctx || !canvas) return;

        // Controle de frame rate para melhor performance
        if (now - lastTimestamp < frameInterval) {
            animationFrameId = requestAnimationFrame(drawMatrix);
            return;
        }
        lastTimestamp = now;

        // Efeito de fade mais suave (para rastro das letras)
        ctx.fillStyle = "rgba(1, 6, 12, 0.1)"; // Fundo mais escuro e suave
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00e0ff";
        ctx.font = `${fontSize}px 'Fira Code', monospace`;
        ctx.globalAlpha = 0.25; // Opacidade ajustada para não competir com a marca d'água

        for (let i = 0; i < drops.length; i++) {
            // Caracteres binários
            const text = binaryChars[Math.floor(Math.random() * binaryChars.length)];
            const x = i * fontSize;
            const y = drops[i] * fontSize;

            // Efeito de brilho nos caracteres
            if (drops[i] % 10 === 0) {
                ctx.globalAlpha = 0.45; // Destaca alguns caracteres
            } else {
                ctx.globalAlpha = 0.25;
            }
            
            ctx.fillText(text, x, y);

            // Reset position when goes off screen
            if (y > canvas.height && Math.random() > 0.98) {
                drops[i] = 0;
            }

            drops[i]++;
        }

        ctx.globalAlpha = 1;
        animationFrameId = requestAnimationFrame(drawMatrix);
    }

    if (canvas && ctx) {
        resizeCanvas();
        initDrops();
        drawMatrix(0); // Iniciar animação

        // Recalcula ao redimensionar (com debounce para performance)
        let resizeTimeout;
        window.addEventListener("resize", () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                resizeCanvas();
                initDrops();
            }, 100);
        });
        
        // Cleanup animation frame on page unload
        window.addEventListener('beforeunload', function() {
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
        });
    }

    // =========================
    // SCROLL ANIMATIONS (OPCIONAL)
    // =========================
    // Animação suave para elementos ao scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.specialty-card, .article-card, .contact-item');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if (elementPosition < screenPosition - 50) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animated elements
    const animatedElements = document.querySelectorAll('.specialty-card, .article-card, .contact-item');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Trigger animation on load and scroll
    setTimeout(animateOnScroll, 100);
    window.addEventListener('scroll', animateOnScroll);
    
    // =========================
    // PREVENT RIGHT CLICK ON IMAGES (OPCIONAL)
    // =========================
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            return false;
        });
    });

    // =========================
    // BACK TO TOP LINK
    // =========================
    const backToTopLink = document.getElementById('backToTop');
    
    if (backToTopLink) {
        // Mostrar/ocultar link ao scroll
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopLink.classList.add('show');
            } else {
                backToTopLink.classList.remove('show');
            }
        });
        
        // Scroll suave ao topo ao clicar
        backToTopLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // =========================
    // ADICIONAR CLASSE ACTIVE NO MENU CONFORME PÁGINA ATUAL
    // =========================
    const currentPage = window.location.pathname.split("/").pop() || "index.html";
    const navLinksItems = document.querySelectorAll('.nav-links a');
    
    navLinksItems.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === "index.html" && href === "/") || (currentPage === "index.html" && href === "index.html")) {
            link.classList.add('active');
        } else if (currentPage !== "index.html" && href === currentPage) {
            link.classList.add('active');
        }
    });
    
    // =========================
    // MARCAR ARTIGO ATIVO NA PÁGINA DE ARTIGOS
    // =========================
    if (currentPage === "artigos.html") {
        const artigosMenuLink = document.querySelector('.nav-links a[href="artigos.html"]');
        if (artigosMenuLink) {
            artigosMenuLink.classList.add('active');
        }
    }
    
    console.log("Site completamente inicializado - Modo Perícia Digital");
});