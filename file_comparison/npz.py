from collections.abc import Iterable
import neo.io


all_failures = {}
known_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, str, bytes, list, dict, bool, float, int, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal,]

def iterable_are_equal (item1, item2, comparison_path):
    keys_to_avoid = []
    common_keys = []
    # print (comparison_path)

    if (type (item1) not in known_types or type(item2) not in known_types):
        print (comparison_path + " " + str(type(item1)) + " " + str(type(item2)))

    #############   NUMPY.NPZ.Files  #################
    # Convert npz files into compatible arrays
    if ((type(item1) == np.lib.npyio.NpzFile) and (type(item2) == np.lib.npyio.NpzFile)):
        # Check keys_to_avoid# # TODO
        for ikey in item1.files:
            if not ikey in item2.files:
                keys_to_avoid.append(ikey)
            elif not ikey in common_keys:
                common_keys.append(ikey)

        for ikey in item2.files:
            if not ikey in item1.files:
                keys_to_avoid.append(ikey)
            elif not ikey in common_keys:
                common_keys.append(ikey)

        # common_keys = item1.files - keys_to_avoid
        if len(keys_to_avoid) >0:
            all_failures[str(comparison_path+str(type(item1))+"->KeysAvoided")] = keys_to_avoid

        # Iterate on keys
        for ivar in common_keys:
            iterable_are_equal(item1[ivar], item2[ivar], comparison_path+str(type(item1))+"->"+str(ivar)+"->")

    #############   NUMPY.arrays  #################
    # Convert numpy arrays into compatible arrays
    elif ((type(item1) == np.ndarray) and (type(item2) == np.ndarray)):
        iterable_are_equal(item1.tolist(), item2.tolist(), comparison_path+str(type(item1))+"->")

    #############   NEO.BLOCK   ###################
    # TODO
    elif (type(item1) == neo.core.block.Block) and (type(item2) == neo.core.block.Block):
        # Convert neo.blocks into compatible arrays
        if (len(item1.segments) != len(item2.segments)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of segments don't have same length"

        for ivar in range( len(item1.segments)):
            iterable_are_equal(item1.segments[ivar], item2.segments[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

    ############    NEO.SEGMENT ##################
    # TODO
    elif (type(item1) == neo.core.Segment) and (type(item2) == neo.core.Segment):
        #############   AnalogSignal    ##############
        if (len(item1.analogsignals) != len(item2.analogsignals)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of AnalogSignal don't have same length"

        if (len(item1.analogsignals)>0):
            for ivar in range (len(item1.analogsignals)):
                iterable_are_equal (item1.analogsignals[ivar], item2.analogsignals[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   SpikeTrain    ##############
        if (len(item1.spiketrains) != len(item2.spiketrains)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of SpikeTrain don't have same length"

        if (len(item1.spiketrains)>0):
            for ivar in range (len(item1.spiketrains)):
                iterable_are_equal (item1.spiketrains[ivar], item2.spiketrains[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   Event    ##############
        if (len(item1.events) != len(item2.events)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of Event don't have same length"

        if (len(item1.events)>0):
            for ivar in range (len(item1.events)):
                iterable_are_equal (item1.events[ivar], item2.events[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   Epoch    ##############
        if (len(item1.epochs) != len(item2.epochs)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of Epoch don't have same length"

        if (len(item1.epochs)>0):
            for ivar in range (len(item1.epochs)):
                iterable_are_equal (item1.epochs[ivar], item2.epochs[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

        #############   IrregularlySampledSignal    ##############
        if (len(item1.irregularlysampledsignals) != len(item2.irregularlysampledsignals)):
            all_failures[str(comparison_path+str(item1.name)+str(type(item1))+"->")] = "List of IrregularlySampledSignal don't have same length"

        if (len(item1.irregularlysampledsignals)>0):
            for ivar in range (len(item1.irregularlysampledsignals)):
                iterable_are_equal (item1.irregularlysampledsignals[ivar], item2.irregularlysampledsignals[ivar], comparison_path+str(item1.name)+str(type(item1))+"->")

    elif ((isinstance(item1, Iterable)) and (isinstance(item2, Iterable)) and (type(item1)!=str) and (type(item1)!= bytes) ):


        #################   LIST    ###################
        if ((type(item1) == list) and (type(item2) == list)):
            if len(item1) != len(item2):
                all_failures[str(comparison_path+str(type(item1))+"->")] = "List don't have same length"
            else:
                for id_ilist in range(len(item1)):
                    iterable_are_equal (item1[id_ilist], item2[id_ilist], comparison_path+str(type(item1))+"->")

        #################   DICT    ###################
        # Check if item1 and item2 provide keys to check keys
        if ((type(item1) == dict) and (type(item2) == dict)):

            for ikey in item1.keys():
                if not ikey in item2:
                    # print ("%s not present in one dataset" %(comparison_path+str(type(item1))+"->" +"->"+ str(ikey)))
                    keys_to_avoid.append(ikey)

            for ikey in item2.keys():
                if not ikey in item1:
                    # print ("%s not present in one dataset" %(comparison_path+str(type(item1))+"->"+"->"+str(ikey)))
                    keys_to_avoid.append(ikey)

            common_keys = item1.keys() - keys_to_avoid
            if len(keys_to_avoid) >0:
                all_failures[str(comparison_path+str(type(item1))+"->KeysAvoided")] = keys_to_avoid

            # Iterate on items of item1 and item2
            for item in common_keys:
                iterable_are_equal(item1[item], item2[item], comparison_path+str(type(item1))+"->"+item+"->")


    # If item1 and item2 are not iterable (are values)
    elif (item1 != item2):
        all_failures[str(comparison_path+str(type(item1))+"->"+str(item1))] = "(delta= TODO)"