<?xml version="1.0" encoding="windows-1250"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:ami="urn:cz:isvs:ruian:schemas:AdrMistoIntTypy:v1"
                xmlns:base="urn:cz:isvs:ruian:schemas:BaseTypy:v1"
                xmlns:coi="urn:cz:isvs:ruian:schemas:CastObceIntTypy:v1"
                xmlns:com="urn:cz:isvs:ruian:schemas:CommonTypy:v1"
                xmlns:kui="urn:cz:isvs:ruian:schemas:KatUzIntTypy:v1"
                xmlns:kri="urn:cz:isvs:ruian:schemas:KrajIntTypy:v1"
                xmlns:mci="urn:cz:isvs:ruian:schemas:MomcIntTypy:v1"
                xmlns:mpi="urn:cz:isvs:ruian:schemas:MopIntTypy:v1"
                xmlns:obi="urn:cz:isvs:ruian:schemas:ObecIntTypy:v1"
                xmlns:oki="urn:cz:isvs:ruian:schemas:OkresIntTypy:v1"
                xmlns:opi="urn:cz:isvs:ruian:schemas:OrpIntTypy:v1"
                xmlns:pai="urn:cz:isvs:ruian:schemas:ParcelaIntTypy:v1"
                xmlns:pui="urn:cz:isvs:ruian:schemas:PouIntTypy:v1"
                xmlns:rsi="urn:cz:isvs:ruian:schemas:RegSouIntiTypy:v1"
                xmlns:spi="urn:cz:isvs:ruian:schemas:SpravObvIntTypy:v1"
                xmlns:sti="urn:cz:isvs:ruian:schemas:StatIntTypy:v1"
                xmlns:soi="urn:cz:isvs:ruian:schemas:StavObjIntTypy:v1"
                xmlns:uli="urn:cz:isvs:ruian:schemas:UliceIntTypy:v1"
                xmlns:vci="urn:cz:isvs:ruian:schemas:VuscIntTypy:v1"
                xmlns:vf="urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1"
                xmlns:zji="urn:cz:isvs:ruian:schemas:ZsjIntTypy:v1"
                xmlns:voi="urn:cz:isvs:ruian:schemas:VOIntTypy:v1">

    <xsl:template match="vf:VymennyFormat">
        <!--  hlavicka zahozena-->
        <vf:VymennyFormat>
            <xsl:apply-templates select="vf:Data"/>
        </vf:VymennyFormat>
    </xsl:template>

    <xsl:template match="vf:Data">
        <vf:Data>
            <vf:Obce>
                <xsl:apply-templates select="vf:Obce"/>
            </vf:Obce>
            <vf:CastiObci>
                <xsl:apply-templates select="vf:CastiObci"/>
            </vf:CastiObci>
            <vf:KatastralniUzemi>
                <xsl:apply-templates select="vf:KatastralniUzemi"/>
            </vf:KatastralniUzemi>
            <vf:Zsj>
                <xsl:apply-templates select="vf:Zsj"/>
            </vf:Zsj>
            <vf:Ulice>
                <xsl:apply-templates select="vf:Ulice"/>
            </vf:Ulice>
            <vf:Parcely>
                <xsl:apply-templates select="vf:Parcely"/>
            </vf:Parcely>
            <vf:StavebniObjekty>
                <xsl:apply-templates select="vf:StavebniObjekty"/>
            </vf:StavebniObjekty>
            <vf:AdresniMista>
                <xsl:apply-templates select="vf:AdresniMista"/>
            </vf:AdresniMista>
        </vf:Data>
    </xsl:template>

    <xsl:template match="vf:Obce">
        <xsl:for-each select="vf:Obec">
            <vf:Obec>
                <obi:Kod>
                    <xsl:value-of select="obi:Kod"/>
                </obi:Kod>
                <obi:Nazev>
                    <xsl:value-of select="obi:Nazev"/>
                </obi:Nazev>
                <obi:StatusKod>
                    <xsl:value-of select="obi:StatusKod"/>
                </obi:StatusKod>
                <obi:Okres>
                    <oki:Kod>
                        <xsl:value-of select="obi:Okres/oki:Kod"/>
                    </oki:Kod>
                </obi:Okres>
                <obi:Pou>
                    <pui:Kod>
                        <xsl:value-of select="obi:Pou/pui:Kod"/>
                    </pui:Kod>
                </obi:Pou>
            </vf:Obec>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:CastiObci">
        <xsl:for-each select="vf:CastObce">
            <vf:CastObce>
                <coi:Kod>
                    <xsl:value-of select="coi:Kod"/>
                </coi:Kod>
                <coi:Nazev>
                    <xsl:value-of select="coi:Nazev"/>
                </coi:Nazev>
                <coi:Obec>
                    <obi:Kod>
                        <xsl:value-of select="coi:Obec/obi:Kod"/>
                    </obi:Kod>
                </coi:Obec>
            </vf:CastObce>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:KatastralniUzemi">
        <xsl:for-each select="vf:KatastralniUzemi">
            <vf:KatastralniUzemi>
                <kui:Kod>
                    <xsl:value-of select="kui:Kod"/>
                </kui:Kod>
                <kui:Nazev>
                    <xsl:value-of select="kui:Nazev"/>
                </kui:Nazev>
                <kui:Obec>
                    <obi:Kod>
                        <xsl:value-of select="kui:Obec/obi:Kod"/>
                    </obi:Kod>
                </kui:Obec>
            </vf:KatastralniUzemi>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Zsj">
        <xsl:for-each select="vf:Zsj">
            <vf:Zsj>
                <zji:Kod>
                    <xsl:value-of select="zji:Kod"/>
                </zji:Kod>
                <zji:Nazev>
                    <xsl:value-of select="zji:Nazev"/>
                </zji:Nazev>
                <zji:KatastralniUzemi>
                    <kui:Kod>
                        <xsl:value-of select="zji:KatastralniUzemi/kui:Kod"/>
                    </kui:Kod>
                </zji:KatastralniUzemi>
                <zji:Vymera>
                    <xsl:value-of select="zji:Vymera"/>
                </zji:Vymera>
            </vf:Zsj>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Ulice">
        <xsl:for-each select="vf:Ulice">
            <vf:Ulice>
                <uli:Kod>
                    <xsl:value-of select="uli:Kod"/>
                </uli:Kod>
                <uli:Nazev>
                    <xsl:value-of select="uli:Nazev"/>
                </uli:Nazev>
                <uli:Obec>
                    <obi:Kod>
                        <xsl:value-of select="uli:Obec/obi:Kod"/>
                    </obi:Kod>
                </uli:Obec>
            </vf:Ulice>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Parcely">
        <xsl:for-each select="vf:Parcela">
            <vf:Parcela>
                <pai:Id>
                    <xsl:value-of select="pai:Id"/>
                </pai:Id>
                <pai:KatastralniUzemi>
                    <kui:Kod>
                        <xsl:value-of select="pai:KatastralniUzemi/kui:Kod"/>
                    </kui:Kod>
                </pai:KatastralniUzemi>
            </vf:Parcela>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:StavebniObjekty">
        <xsl:for-each select="vf:StavebniObjekt">
            <vf:StavebniObjekt>
                <soi:Kod>
                    <xsl:value-of select="soi:Kod"/>
                </soi:Kod>
                <soi:CislaDomovni>
                    <com:CisloDomovni>
                        <xsl:value-of select="soi:CislaDomovni/com:CisloDomovni"/>
                    </com:CisloDomovni>
                </soi:CislaDomovni>
                <soi:IdentifikacniParcela>
                    <pai:Id>
                        <xsl:value-of select="soi:IdentifikacniParcela/pai:Id"/>
                    </pai:Id>
                </soi:IdentifikacniParcela>
                <soi:TypStavebnihoObjektuKod>
                    <xsl:value-of select="soi:TypStavebnihoObjektuKod"/>
                </soi:TypStavebnihoObjektuKod>
                <soi:ZpusobVyuzitiKod>
                    <xsl:value-of select="soi:ZpusobVyuzitiKod"/>
                </soi:ZpusobVyuzitiKod>
                <soi:CastObce>
                    <coi:Kod>
                        <xsl:value-of select="soi:CastObce/coi:Kod"/>
                    </coi:Kod>
                </soi:CastObce>
                <soi:PocetBytu>
                    <xsl:value-of select="soi:PocetBytu"/>
                </soi:PocetBytu>
                <soi:PocetPodlazi>
                    <xsl:value-of select="soi:PocetPodlazi"/>
                </soi:PocetPodlazi>
                <soi:PodlahovaPlocha>
                    <xsl:value-of select="soi:PodlahovaPlocha"/>
                </soi:PodlahovaPlocha>
                <soi:PripojeniKanalizaceKod>
                    <xsl:value-of select="soi:PripojeniKanalizaceKod"/>
                </soi:PripojeniKanalizaceKod>
                <soi:PripojeniPlynKod>
                    <xsl:value-of select="soi:PripojeniPlynKod"/>
                </soi:PripojeniPlynKod>
                <soi:PripojeniVodovodKod>
                    <xsl:value-of select="soi:PripojeniVodovodKod"/>
                </soi:PripojeniVodovodKod>
                <soi:VybaveniVytahemKod>
                    <xsl:value-of select="soi:VybaveniVytahemKod"/>
                </soi:VybaveniVytahemKod>
                <soi:ZpusobVytapeniKod>
                    <xsl:value-of select="soi:ZpusobVytapeniKod"/>
                </soi:ZpusobVytapeniKod>
            </vf:StavebniObjekt>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:AdresniMista">
        <xsl:for-each select="vf:AdresniMisto">
            <vf:AdresniMisto>
                <ami:Kod>
                    <xsl:value-of select="ami:Kod"/>
                </ami:Kod>
                <ami:CisloDomovni>
                    <xsl:value-of select="ami:CisloDomovni"/>
                </ami:CisloDomovni>
                <ami:Psc>
                    <xsl:value-of select="ami:Psc"/>
                </ami:Psc>
                <ami:StavebniObjekt>
                    <soi:Kod>
                        <xsl:value-of select="ami:StavebniObjekt/soi:Kod"/>
                    </soi:Kod>
                </ami:StavebniObjekt>
            </vf:AdresniMisto>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>