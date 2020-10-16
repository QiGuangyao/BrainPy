# -*- coding: utf-8 -*-

import npbrain as nb
import npbrain.numpy as np


def GapJunction():
    requires = dict(
        ST=nb.types.SynState(
            ['s', 'w'],
            help='''
            Gap junction state.

            s : conductance for post-synaptic neuron.
            w : gap junction conductance.
            '''
        ),
        pre=nb.types.NeuState(['V']),
        post=nb.types.NeuState(['V', 'inp']),
        post2syn=nb.types.ListConn(help='post-to-synapse connection.'),
        pre_ids=nb.types.Array(dim=1, help='Pre-synaptic neuron indices.'),
    )

    def update(ST, pre, post, post2syn, pre_ids):
        num_post = len(post2syn)
        for post_id in range(num_post):
            for syn_id in post2syn[post_id]:
                pre_id = pre_ids[syn_id]
                post['inp'][post_id] = ST['w'][syn_id] * (pre['V'][pre_id] - post['V'][post_id])

    return nb.SynType(name='GapJunction', requires=requires, steps=update, vector_based=True)


def gap_junction_lif(spikelet=0.1):
    requires = dict(
        ST=nb.types.SynState(
            ['spikelet', 'w'],
            help='''
                Gap junction state.

                s : conductance for post-synaptic neuron.
                w : gap junction conductance. It
                '''
        ),
        pre=nb.types.NeuState(['V', 'sp']),
        post=nb.types.NeuState(['V', 'inp']),
        post2syn=nb.types.ListConn(help='post-to-synapse connection.'),
        pre_ids=nb.types.Array(dim=1, help='Pre-synaptic neuron indices.'),
    )

    def update(ST, pre, post, post2syn, pre_ids):
        num_post = len(post2syn)
        for post_id in range(num_post):
            for syn_id in post2syn[post_id]:
                pre_id = pre_ids[syn_id]
                post['inp'][post_id] += ST['w'] * (pre['V'][pre_id] - post['V'][post_id])
                ST['spikelet'][syn_id] = ST['w'][syn_id] * spikelet * pre['sp']

    @nb.delayed
    def output(ST, post, post2syn):
        post_spikelet = np.zeros(len(post2syn), dtype=np.float_)
        for post_id, syn_ids in enumerate(post2syn):
            post_spikelet[post_id] = np.sum(ST['spikelet'][syn_ids])
        post['V'] += post_spikelet

    return nb.SynType(name='GapJunctin_for_LIF', requires=requires, steps=update, vector_based=True)


