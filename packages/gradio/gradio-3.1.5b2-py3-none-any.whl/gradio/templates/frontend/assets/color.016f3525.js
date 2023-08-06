import { ae as ordered_colors } from './index.6dad4e0b.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
