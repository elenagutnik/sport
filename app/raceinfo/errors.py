class BibRepeat(Exception):
   def __init__(self, competitor_name, bib):
      self.competitor_name = competitor_name
      self.bib = bib

   def __str__(self):
      return 'The race has alreagy have competitor with given bib (competitor %s, bib %s)' % (self.competitor_name,
                                                                                              self.bib)