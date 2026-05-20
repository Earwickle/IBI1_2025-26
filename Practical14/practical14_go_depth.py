import os
import xml.dom.minidom as minidom
import xml.sax
from datetime import datetime


TARGET_NAMESPACES = {
    'molecular_function',
    'biological_process',
    'cellular_component',
}


def parse_dom(path):
    doc = minidom.parse(path)
    terms = doc.getElementsByTagName('term')
    results = {}
    for term in terms:
        ns_elems = term.getElementsByTagName('namespace')
        if not ns_elems:
            continue
        namespace = ''.join(n.nodeValue for n in ns_elems[0].childNodes if n.nodeType == n.TEXT_NODE).strip()
        if namespace not in TARGET_NAMESPACES:
            continue
        name_elems = term.getElementsByTagName('name')
        name = ''
        if name_elems:
            name = ''.join(n.nodeValue for n in name_elems[0].childNodes if n.nodeType == n.TEXT_NODE).strip()
        is_a_elems = term.getElementsByTagName('is_a')
        count = len(is_a_elems)
        if namespace not in results or count > results[namespace][1]:
            results[namespace] = (name, count)
    return results


class GOHandler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.in_term = False
        self.current_name = ''
        self.current_namespace = ''
        self.capturing = None
        self.current_is_a_count = 0
        self.results = {}

    def startElement(self, name, attrs):
        if name == 'term':
            self.in_term = True
            self.current_name = ''
            self.current_namespace = ''
            self.current_is_a_count = 0
        elif self.in_term and name in ('name', 'namespace'):
            self.capturing = name
        elif self.in_term and name == 'is_a':
            # count every is_a occurrence inside a term
            self.current_is_a_count += 1

    def characters(self, content):
        if not self.in_term or not self.capturing:
            return
        if self.capturing == 'name':
            self.current_name += content
        elif self.capturing == 'namespace':
            self.current_namespace += content

    def endElement(self, name):
        if name in ('name', 'namespace'):
            self.capturing = None
        if name == 'term':
            ns = self.current_namespace.strip()
            if ns in TARGET_NAMESPACES:
                n = self.current_name.strip()
                c = self.current_is_a_count
                if ns not in self.results or c > self.results[ns][1]:
                    self.results[ns] = (n, c)
            self.in_term = False


def parse_sax(path):
    handler = GOHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    with open(path, 'r', encoding='utf-8') as fh:
        parser.parse(fh)
    return handler.results


def main():
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'go_obo.xml')
    if not os.path.exists(path):
        print('Could not find go_obo.xml in', here)
        return

    t0 = datetime.now()
    dom_results = parse_dom(path)
    t1 = datetime.now()
    sax_results = parse_sax(path)
    t2 = datetime.now()

    dom_time = (t1 - t0).total_seconds()
    sax_time = (t2 - t1).total_seconds()

    print('DOM parse time: {:.6f} s'.format(dom_time))
    print('SAX parse time: {:.6f} s'.format(sax_time))

    print('\nResults (term with most <is_a> per ontology):')
    for ns in sorted(TARGET_NAMESPACES):
        dom_val = dom_results.get(ns, ('(none)', 0))
        sax_val = sax_results.get(ns, ('(none)', 0))
        # print DOM results (they should match SAX)
        print(f"- {ns}: {dom_val[0]} ({dom_val[1]} is_a)")

    if dom_time < sax_time:
        faster = 'DOM'
    elif sax_time < dom_time:
        faster = 'SAX'
    else:
        faster = 'equal'

    print('\nFastest API:', faster)


if __name__ == '__main__':
    main()

# Comment: SAX was fastest on this run (measured SAX < DOM).