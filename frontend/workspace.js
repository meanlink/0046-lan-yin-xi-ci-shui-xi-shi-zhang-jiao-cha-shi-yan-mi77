import {mount} from './base.js';
import {render as edition} from './edition_page.js';
import {render as pairs} from './pairs_page.js';
import {render as assay} from './assay_page.js';
import {render as recipe} from './recipe_page.js';
const pages = {"edition": "试印版簿", "pairs": "配对试条", "assay": "置换比对", "recipe": "定版工签"};
const screens = {edition, pairs, assay, recipe};
mount({title: "蓝印洗次 · 水洗时长交叉实验", kicker: "栖浦暗房试印册", pages, render: (page, outlet, user) => screens[page](outlet, user)});
