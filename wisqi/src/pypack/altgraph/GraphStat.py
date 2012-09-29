'''
Functions providing various graph statistics
'''
import sys

def avg_hops(graph):
    '''

    '''
    pass

def degree_dist(graph, limits=(0,0), bin_num=10, mode='out'):
    '''
    Computes the degree distribution for a graph.
    Returns a list of tuples where the first element of the tuple is the center of the bin
    representing a range of degrees and the second element of the tuple are the number of nodes
    with the degree falling in the range.

    Example::
        ....

    '''

    deg = []
    if mode == 'inc':
        get_deg = graph.inc_degree
    else:
        get_deg = graph.out_degree

    for node in graph:
        deg.append( graph.get_degree(node) )

    results = _binning(values=deg, limits=limits, bin_num=bin_num)

    return results

def _binning(values, limits=(0,0), bin_num=10):
    '''
    Bins data that falls between certain limits.
    Returns a list of tuples where the first element of the tuple is the center of the bin
    and the second element of the tuple are the counts.
    '''
    if limits == (0, 0):
        eps = 1.0/sys.maxint
        min_val, max_val = min(values) - eps, max(values) + eps
    else:
        min_val, max_val = limits

    # get bin size
    bin_size = (max_val - min_val)/float(bin_num)
    bins = [0] * (bin_num)

    # will ignore these outliers for now
    out_points = 0
    for value in values:
        try:
            if (value - min_val) < 0:
                out_points += 1
            else:
                index = int((value - min_val)/float(bin_size))
                bins[index] += 1
        except:
            out_points += 1

    # make it ready for an x,y plot
    result = []
    center = (bin_size/2) + min_val
    for i, y in enumerate(bins):
        x = center + bin_size * i
        result.append( (x,y) )

    return result


if __name__ == '__main__':
    a = range(100)
    out = _binning(a, limits = (0, 0) )
    print out
