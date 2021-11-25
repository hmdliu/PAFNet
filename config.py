import sys
from addict import Dict
from copy import deepcopy

def get_config(dataset, info):

    # backbone, epochs, _ = tuple(info.split('_'))
    # assert dataset in ('nyud', 'sunrgbd')
    # assert backbone in ('res18', 'res50')
    # assert epochs.isdigit()
    # config = deepcopy(Dict(TEMPLATE))
    # config.training.export = True
    # config.training.epochs = int(epochs)
    # config.training.dataset = dataset
    # config.general.encoder = backbone

    date, setting = tuple(info.split('_'))
    config = deepcopy(Dict(TEMPLATE))
    config.training.epochs = 600
    config.training.dataset = dataset
    config.general.encoder = 'res18'
    config.decoder_args.aux = False

    if date == '1125':
        # decoder: simple add
        config.decoder_args.lf_args.conv_flag = (False, False)
        config.decoder_args.lf_args.lf_bb = 'none'
        config.decoder_args.lf_args.fuse_args = {
            'fuse_setting': {
                'merge_mode': 'add',
                'init': False,
                'civ': None
            },
            'att_module': 'idt',
            'att_setting': {}
        }

        # default encoder: CPAF+, d = 8, m = 16, sp = u
        # n: CPAF; p: CPAF+
        assert setting[0] in ('n', 'p')
        if setting[0] == 'n':
            config.encoder_args.fuse_args.descriptor = -1
        # pyramid pooling size
        size_dict = {
            'a': (1, ),
            'b': (1, 2),
            'c': (1, 2, 4),
            'd': (1, 2, 4, 8)
        }
        assert setting[1] in size_dict
        config.encoder_args.fuse_args.pp_size = size_dict[setting[1]]
    else:
        raise ValueError('Invalid date: %s' % date)
    
    return config

def test_config():
    config = get_config(sys.argv[1], sys.argv[2])
    for k, v in config.items():
        print('[%s]: %s' % (k, v))

TEMPLATE = {
    'training': {
        # Dataset
        'dataset': None,
        'workers': 4,
        'base_size': 520,
        'crop_size': 480,
        'train_split': 'train',
        'export': False,
        # Aux loss
        'aux_weight': 0.5,
        'class_weight': 1,
        # Training setting
        'epochs': None,
        'batch_size': 8,
        'test_batch_size': 8,
        'lr': 0.003,
        'lr_scheduler': 'poly',
        'momentum': 0.9,
        'weight_decay': 0.0001,
        'use_cuda': True,
        'seed': 1,
    },
    'general': {
        'encoder': None,
        'feats': 'x'
    },
    'encoder_args': {
        'fuse_args': {
            'pp_size': (1, 2, 4, 8),
            'descriptor': 8,
            'mid_feats': 16,
            'sp_feats': 'u'
        },
        'pass_rff': (True, False),
        'fuse_module': 'cpaf'
    },
    'decoder_args': {
        'aux': True,
        'final_aux': False,
        'lf_args': {
            'conv_flag': (True, False),
            'lf_bb': 'irb[2->2]',
            'fuse_args': {
                'fuse_setting': {
                    'merge_mode': 'grp',
                    'init': True,
                    'civ': 0.5
                },
                'att_module': 'rpa',
                'att_setting': {
                    'pp_layer': 4,
                    'descriptor': 8,
                    'mid_feats': 16,
                }
            },
            'fuse_module': 'mgf'
        },
    }
}


if __name__ == '__main__':
    test_config()