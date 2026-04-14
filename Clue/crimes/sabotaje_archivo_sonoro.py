"""
sabotaje_archivo_sonoro.py — El Sabotaje en el Archivo Sonoro

En la Fonoteca Nacional se borró la restauración final de una grabación histórica pocas horas antes de su presentación pública.
El borrado no pudo hacerse de forma remota; solo era posible desde la consola interna del laboratorio de audio.
La Restauradora Inés tenía acceso autorizado al laboratorio esa noche.
El Ingeniero Barros también tenía acceso autorizado y su tarjeta fue registrada en la puerta del laboratorio durante el intervalo del sabotaje.
La Catalogadora Nerea participaba al mismo tiempo en una reunión virtual con otra sede y su conexión quedó registrada.
El Pasante Elías no tenía permisos de acceso al laboratorio de audio.
Los registros del sistema muestran que la sesión del Ingeniero Barros ejecutó la eliminación del archivo maestro.
La Catalogadora Nerea acusó al Ingeniero Barros.
El Ingeniero Barros afirmó que Inés estuvo con él toda la noche revisando equipos.
La Restauradora Inés afirmó que Barros estuvo con ella toda la noche revisando equipos.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene coartada verificada queda descartado.
Quien no tiene acceso al laboratorio no pudo cometer el sabotaje.
Quien ejecutó la eliminación del archivo maestro tiene evidencia digital en su contra.
Quien tenía acceso al laboratorio y tiene evidencia digital en su contra es culpable.
El testimonio de una persona descartada es confiable.
Quien da coartada a un culpable lo está encubriendo.
Si dos personas se dan coartada mutuamente, existe una coartada cruzada entre ellas.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    restauradora_ines = Term("restauradora_ines")
    ingeniero_barros = Term("ingeniero_barros")
    catalogadora_nerea = Term("catalogadora_nerea")
    pasante_elias = Term("pasante_elias")
    laboratorio_audio = Term("laboratorio_audio")
    archivo_maestro = Term("archivo_maestro")

    persona = Term("$X")
    otra_persona = Term("$Y")
    lugar = Term("$L")
    archivo = Term("$A")

    kb.add_fact(Predicate("acceso_autorizado", (restauradora_ines, laboratorio_audio)))
    kb.add_fact(Predicate("acceso_autorizado", (ingeniero_barros, laboratorio_audio)))

    kb.add_fact(Predicate("coartada_verificada", (catalogadora_nerea,)))
    kb.add_fact(Predicate("sin_acceso", (pasante_elias, laboratorio_audio)))

    kb.add_fact(Predicate("registro_en_lugar", (ingeniero_barros, laboratorio_audio)))
    kb.add_fact(Predicate("elimino_archivo", (ingeniero_barros, archivo_maestro)))
    kb.add_fact(Predicate("archivo_objetivo", (archivo_maestro,)))

    kb.add_fact(Predicate("acusa", (catalogadora_nerea, ingeniero_barros)))

    kb.add_fact(Predicate("da_coartada", (ingeniero_barros, restauradora_ines)))
    kb.add_fact(Predicate("da_coartada", (restauradora_ines, ingeniero_barros)))

    kb.add_rule(
        Rule(
            Predicate("descartado", (persona,)),
            (Predicate("coartada_verificada", (persona,)),)
        )
    )

    kb.add_rule(
        Rule(
            Predicate("descartado", (persona,)),
            (Predicate("sin_acceso", (persona, lugar)),)
        )
    )

    kb.add_rule(
        Rule(
            Predicate("evidencia_digital", (persona,)),
            (
                Predicate("elimino_archivo", (persona, archivo)),
                Predicate("archivo_objetivo", (archivo,))
            )
        )
    )

    kb.add_rule(
        Rule(
            Predicate("culpable", (persona,)),
            (
                Predicate("acceso_autorizado", (persona, laboratorio_audio)),
                Predicate("evidencia_digital", (persona,))
            )
        )
    )

    kb.add_rule(
        Rule(
            Predicate("testimonio_confiable", (persona, otra_persona)),
            (
                Predicate("descartado", (persona,)),
                Predicate("acusa", (persona, otra_persona))
            )
        )
    )

    kb.add_rule(
        Rule(
            Predicate("encubridor", (persona,)),
            (
                Predicate("da_coartada", (persona, otra_persona)),
                Predicate("culpable", (otra_persona,))
            )
        )
    )

    kb.add_rule(
        Rule(
            Predicate("coartada_cruzada", (persona, otra_persona)),
            (
                Predicate("da_coartada", (persona, otra_persona)),
                Predicate("da_coartada", (otra_persona, persona))
            )
        )
    )

    return kb


CASE = CrimeCase(
    id="sabotaje_archivo_sonoro",
    title="El Sabotaje en el Archivo Sonoro",
    suspects=("restauradora_ines", "ingeniero_barros", "catalogadora_nerea", "pasante_elias"),
    narrative=__doc__,
    description=(
        "En una fonoteca se eliminó la restauración final de una grabación histórica desde la consola interna "
        "del laboratorio. Un sospechoso tenía acceso y evidencia digital directa."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿El Ingeniero Barros es culpable?",
            goal=Predicate("culpable", (Term("ingeniero_barros"),)),
        ),
        QuerySpec(
            description="¿La Catalogadora Nerea está descartada?",
            goal=Predicate("descartado", (Term("catalogadora_nerea"),)),
        ),
        QuerySpec(
            description="¿El Pasante Elías está descartado?",
            goal=Predicate("descartado", (Term("pasante_elias"),)),
        ),
        QuerySpec(
            description="¿El testimonio de Nerea contra Barros es confiable?",
            goal=Predicate("testimonio_confiable", (Term("catalogadora_nerea"), Term("ingeniero_barros"))),
        ),
        QuerySpec(
            description="¿Existe coartada cruzada entre Inés y Barros?",
            goal=ExistsGoal("$X", Predicate("coartada_cruzada", (Term("$X"), Term("ingeniero_barros")))),
        ),
    ),
)