# Table of Contents [[toc]{.smallcaps}]{.tag tag-name="toc"} {#table-of-contents}

-   [Vy Learns with
    Spaced-Repetition](#vy-learns-with-spaced-repetition)
-   [Requirements](#requirements)
-   [Usage](#usage)

# Vy Learns with Spaced-Repetition

Vy has recently familiarized herself with the computer keyboard and is
now tackling some Leetcode problems. However, she frequently struggles
to recall the problems she has solved before. Consequently, she requires
assistance from a management system.

This approach involves keeping track of several parameters relating the
learning and a basic version of the Leitner system, enhanced by
incorporating time-awareness. In other words, it utilizes distinct
Leitner systems tailored for various time intervals.

The project is implemented in Python which is easily hackable by
Leetcode users. It can be used for studying other subjects than solving
Leetcode problems.

# Requirements

The Python implementation does not require any additional packages.
However, to use the leetcode-scripts, it requires `Neovide`
(a text editor) and `fzf` (a fuzzy search) to quickly browser
problems.

# Usage

All commands can be skipped with ESC.

Relevant directories:

-   Study results are stored in
    `subjects/sbj-leetcode/study/`
-   Added problems are stored in
    `subject/sbj-leetcode/item/item.json`
-   Parameters related to the learning are stored in
    `subject/sbj-leetcode/tracker/tracker.json`

In the `leetcode-scripts` direction, run

  Command                                 Description
  --------------------------------------- ----------------------------------------------------------------------------
  `vy-learn-leetcode`          initializing the leetcode project by generating necessary directories
  `vy-add`                     add a problem to solve from `problem-lists.txt`
  `vy-start -i {problem_id}`   same as `vy-add` but with provided `problem_id`
  `vy-end`                     complete a problem with result (if successfully or not in solving problem)
  `vy-cancel`                  cancel solving a problem
  `vy-note`                    select a problem to add a note (or retrieve previous note)
  `vy-note -i {problem_i}`     same as `vy-note`, but with a provided `problem_id`
  `vy-list`                    list added problems
  `vy-list-new`                list added, but not attempted, problems
  `vy-list-pass`               list solved problems by \# of successfully solving the problem
  `vy-list-studying`           list pending problems
  `vy-list-duration`           list solved problems by time spent solving
  `vy-list-recent-study`       list solved problems by the most recent attempt
  `vy-add-tag {tag}`           add a tag to a problem
  `vy-remove-tag {tag}`        remove a tag from a problem
  `vy-suggest`                 suggest some solved problems for reviews (using the Leitner system)
