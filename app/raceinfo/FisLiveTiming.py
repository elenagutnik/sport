

class FisLiveTiming:
    def next_at_start(self):
        """
        <raceevent>
        <nextstart bib="1">
        < !-- Startsin must be NOT send with a interval bellow 15 seconds -->
        <startsin> <time>75</time>
        </startsin> </nextstart>
        </raceevent>
        """

    def started(self):
        """<raceevent>
            <start bib="1"/>
            </raceevent>
        """

    def did_not_start(self):
        """Did not start
        <raceevent>
        <dns bib="1"/>
        </raceevent>
        """

    def did_not_finish(self):
        """Did not finish
        <raceevent>
        <dnf bib="1"/>
        </raceevent>
        """

    def diisqualified(self):
        """Diisqualified
        <raceevent>
        <dq bib="1"/>
        </raceevent>
        """
    def speed(self):
        """Intermediate time
        Speed
        <raceevent>
        <speed s="1" bib="3">
        <speed>72.4</speed> </speed>
        </raceevent>
        """
    def intermediat_time(self):
        """Intermediate time
        <raceevent>
        <inter i="1" bib="1">
        <time>19.82</time> <diff>0.00</diff> <rank>1</rank>
        </inter> </raceevent>
        """
    def finish(self):
        """
        <raceevent>
        <finish bib="2">
        <time>1:03.46</time> <diff>0.00</diff>
        <rank>1</rank> </finish>
        </raceevent>
        """
    def correction(self):
        """
        <raceevent>
        <inter i="1" bib="1"correction="y">
        <time>19.82</time> <diff>0.00</diff> <rank>1</rank>
        </inter> </raceevent>
        """
    def correction_erase_a_time(self):
        """
        <raceevent>
        <inter i="1" bib="1"correction="y">
        <time>0.00</time> </inter>
        </raceevent>
        """
    def keepalive(self):
        """
        <livetiming codex="1234" passwd="xxxx" secquence="00005" timstamp="10:21:24">
            <keepalive/>
        </livetiming>
        """

