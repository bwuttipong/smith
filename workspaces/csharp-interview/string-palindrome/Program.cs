// ============================================================
// C# Interview Question - Top 5 Coding Questions #2
// "Write a program in C# to find if a given string is a palindrome or not"
// Source: SimplyLearn - C# Interview Questions and Answers
// ============================================================

using System;

namespace CSharpInterview
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter a string to check if it's a palindrome:");
            string input = Console.ReadLine();

            if (IsPalindrome(input))
                Console.WriteLine($"\"{input}\" is a palindrome.");
            else
                Console.WriteLine($"\"{input}\" is not a palindrome.");
        }

        static bool IsPalindrome(string input)
        {
            // Normalize: ignore case and whitespace for a fair check
            string normalized = input.Replace(" ", "").ToLower();

            int left = 0;
            int right = normalized.Length - 1;

            while (left < right)
            {
                if (normalized[left] != normalized[right])
                    return false;
                left++;
                right--;
            }
            return true;
        }
    }
}